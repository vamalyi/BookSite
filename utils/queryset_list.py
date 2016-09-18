import inspect
from itertools import chain

from django.utils import six
from django.db.models import QuerySet


class BaseQuerySetList(object):

    @classmethod
    def _get_queryset_methods(cls, queryset_class):
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                return self.__class__(map(lambda a: getattr(a, name)(*args, **kwargs), iter(self)))
            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method

        new_methods = {}
        # Refs http://bugs.python.org/issue1785.
        predicate = inspect.isfunction if six.PY3 else inspect.ismethod
        for name, method in inspect.getmembers(queryset_class, predicate=predicate):
            # Only copy missing methods.
            if hasattr(cls, name):
                continue
            # Only copy public methods or methods with the attribute `queryset_only=False`.
            queryset_only = getattr(method, 'queryset_only', None)
            if queryset_only or (queryset_only is None and name.startswith('_')):
                continue
            # Copy the method onto the manager.
            new_methods[name] = create_method(name, method)
        return new_methods

    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        class_dict = {
            '_queryset_class': queryset_class,
        }
        class_dict.update(cls._get_queryset_methods(queryset_class))
        return type(class_name, (cls,), class_dict)


class QuerySetList(list, BaseQuerySetList.from_queryset(QuerySet)):

    def append(self, p_object):
        if type(p_object) != QuerySet:
            raise Exception('object should be QuerySet')
        super().append(p_object)

    def chain(self):
        return list(chain(*iter(self)))

    def count(self, *args, **kwargs):
        return self.__class__(map(lambda a: a.count(*args, **kwargs), iter(self)))