import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.functions import Coalesce
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import Q, F, ExpressionWrapper
from django.db import models

from search.signals import user_search
from utils.queryset_list import QuerySetList
from webshop.models import Product, Category, Manufacturer, BookSeries, ProductParameterValue, Author


class SearchMixin:
    def get(self, request, *args, **kwargs):
        self.params = dict(request.GET)
        self.ordering = self.params.pop('order', ['weight'])
        if self.ordering[0] == "price_ASC":
            self.ordering = ("default_price_sm", "default_price", "asc")
        elif self.ordering[0] == "price_DESC":
            self.ordering = ("default_price_sm", "default_price", "desc")
        elif self.ordering[0] == "date_ASC":
            self.ordering = "-date_on_add"
        elif self.ordering[0] == "date_DESC":
            self.ordering = "date_on_add"
        elif self.ordering [0] == "name_ASC":
            self.ordering = "name"
        elif self.ordering [0] == "name_DESC":
            self.ordering = "-name"
        else:
            self.ordering = self.ordering[0]
        return super().get(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        product_on_page = self.request.COOKIES.get('product_on_page', self.paginate_by)
        if product_on_page == 'all':
            return self.object_list.count()
        return product_on_page

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['product_on_page'] = self.request.COOKIES.get('product_on_page', self.paginate_by)
        ctx['order'] = self.get_ordering()

        return ctx

    def get_ordering(self):
        if type(self.ordering) == tuple:
            if self.ordering[-1] == 'asc':
                ordering = self.ordering[0]
            else:
                ordering = '-{}'.format(self.ordering[0])
        else:
            ordering = self.ordering
        return ordering

    def order_products(self, products):
        if type(self.ordering) == tuple:
            if self.ordering[-1] == 'asc':
                products = products.order_by(Coalesce(*self.ordering[:-1]).asc())
            else:
                products = products.order_by(Coalesce(*self.ordering[:-1]).desc())
        else:
            products = products.order_by(self.ordering)

        return products


class SearchView(SearchMixin, ListView):
    model = Product
    template_name = 'search/results.html'
    context_object_name = 'products'
    paginate_by = settings.PRODUCT_ON_PAGE
    paginate_orphans = 3

    def get(self, request, *args, **kwargs):
        self.search_query = request.GET.get('q', '')
        self.category_id = request.GET.get('category', None)

        user_search.send(sender=self, session=request.session, user=request.user, query=self.search_query)

        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            query = request.META.get('QUERY_STRING')
            return HttpResponseRedirect('{}?{}'.format(reverse('search:search'), re.sub('&?page=([^&]*)', '', query)))

    def filter_products(self, products, category_id=None):
        base_products = products
        products_article = base_products.filter(Q(code__icontains=self.search_query) |
                                                Q(article__icontains=self.search_query))
        products = base_products.exclude(id__in=products_article).filter(name__icontains=self.search_query)
        tags_products = base_products.exclude(
            Q(id__in=products) | Q(id__in=products_article)).filter(
            Q(tags__icontains=self.search_query) | Q(authors__name__icontains=self.search_query) |
              Q(series__name__icontains=self.search_query)
        )
        params_product_ids = ProductParameterValue.objects.filter(
            value__value__icontains=self.search_query).order_by('product_id').distinct(
            'product_id').values_list('product_id', flat=True)
        params_products = base_products.exclude(
            Q(id__in=products) | Q(id__in=products_article) |
            Q(id__in=tags_products)).filter(id__in=params_product_ids
        )
        other = base_products.exclude(
            Q(id__in=products) | Q(id__in=products_article) |
            Q(id__in=tags_products) | Q(id__in=params_products)).filter(
            Q(first_text__icontains=self.search_query) | Q(second_text__icontains=self.search_query))

        products_qs_list = QuerySetList()

        products_qs_list.append(products_article)
        products_qs_list.append(products)
        products_qs_list.append(tags_products)
        products_qs_list.append(params_products)
        products_qs_list.append(other)

        if category_id:
            try:
                products_qs_list = products_qs_list.filter(category=Category.objects.get(pk=category_id))
            except (TypeError, ValueError):
                pass

        products_qs_list = products_qs_list.select_related(
            'sale', 'special_proposition', 'category').prefetch_related('images', 'price_correctors')

        return products_qs_list

    def get_queryset(self):

        if not self.search_query or len(self.search_query) < 3:
            return []

        products_qs_list = self.filter_products(super().get_queryset(), self.category_id).distinct() # 1_part, + distinct()
        products_qs_list = products_qs_list.order_by('weight')

        products = products_qs_list.chain()

        return products

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['search_query'] = self.search_query
        if self.search_query and len(self.search_query) > 2:
            products_qs_list = self.filter_products(Product.objects.all())
            _categories = products_qs_list.distinct(
                'category__name', 'category__id').values_list('category__name', 'category__id')
            categories = list()
            ctx['categories'] = list(set(_categories.chain()))
            for category in ctx['categories']:
                categories.append((category[0], category[1],
                                   sum(products_qs_list.filter(category=Category.objects.get(pk=category[1])).distinct().count()))) # 1_part, + distinct()
            ctx['categories'] = categories
            ctx['products_count'] = sum(products_qs_list.distinct().count()) # 1_part, + distinct()
        try:
            ctx['current_category_id'] = int(self.category_id)
        except (TypeError, ValueError):
            pass

        return ctx


class AuthorFilterView(SearchMixin, ListView):
    model = Product
    template_name = 'search/author_filter.html'
    context_object_name = 'products'
    paginate_by = settings.PRODUCT_ON_PAGE
    paginate_orphans = 3

    def get_queryset(self):
        author_slug = self.kwargs.get('mfa')
        products = super().get_queryset().filter(authors__slug=author_slug)
        products = products.annotate(
            default_price_sm=ExpressionWrapper(
                F('default_price') * F('provider__coefficient') * (1 - F('sale__percent') / 100),
                output_field=models.DecimalField(decimal_places=2, max_digits=12)
            ),
        )
        products = products.select_related(
            'sale', 'special_proposition', 'category').prefetch_related(
            'images', 'price_correctors', 'parameter_values',
            'parameter_values__product_parameter', 'parameter_values__value', )

        return self.order_products(products)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        author_slug = self.kwargs.get('mfa')
        try:
            ctx['author'] = Author.objects.get(slug=author_slug)
        except Exception:
            pass

        return ctx


class SeriesFilterView(SearchMixin, ListView):
    model = Product
    template_name = 'search/series_filter.html'
    context_object_name = 'products'
    paginate_by = settings.PRODUCT_ON_PAGE
    paginate_orphans = 3

    def get_queryset(self):
        mfa_slug = self.kwargs.get('mfa')
        products = super().get_queryset().filter(series__slug=mfa_slug)
        products = products.annotate(
            default_price_sm=ExpressionWrapper(
                F('default_price') * F('provider__coefficient') * (1 - F('sale__percent') / 100),
                output_field=models.DecimalField(decimal_places=2, max_digits=12)
            ),
        )
        products = products.select_related(
            'sale', 'special_proposition', 'category').prefetch_related(
            'images', 'price_correctors', 'parameter_values',
            'parameter_values__product_parameter', 'parameter_values__value', )

        return self.order_products(products)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        mfa_slug = self.kwargs.get('mfa')
        try:
            ctx['series'] = BookSeries.objects.get(slug=mfa_slug)
        except Exception:
            pass

        return ctx


class ProductSearchByParameterValueView(SearchMixin, ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = settings.PRODUCT_ON_PAGE
    paginate_orphans = 3
    template_name = 'search/parameter.html'

    def get(self, request, *args, **kwargs):

        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            query = request.META.get('QUERY_STRING')
            return HttpResponseRedirect(
                '{}?{}'.format(reverse('search:parameter'), re.sub('&?page=([^&]*)', '', query)))

    def get_queryset(self):
        q = self.request.GET.get('q')
        category_id = self.request.GET.get('category')

        if q:
            qs = super().get_queryset().filter(parameter_values__value__value__iexact=q)
            self.all_products = qs
            if category_id:
                qs = qs.filter(category_id=category_id)
            return qs
        return []

    def get_context_data(self, **kwargs):
        category_id = self.request.GET.get('category')
        ctx = dict()

        if self.request.GET.get('q'):
            products = self.all_products.order_by('category_id', 'category__name')
            categories = products.distinct('category_id', 'category__name').values_list('category_id', 'category__name')
            ctx['categories'] = list()
            for c in categories:
                ctx['categories'].append((c[1], c[0], products.filter(category_id=c[0]).count()))
            ctx['products_count'] = products.count()
            ctx['current_category_id'] = int(category_id) if category_id else None
            ctx['search_query'] = self.request.GET.get('q')

        ctx.update(kwargs)

        return super().get_context_data(**ctx)


class AuthorListView(ListView):
    model = Author
    template_name = 'search/manufacturer_list.html'
    context_object_name = 'manufacturer_list'
