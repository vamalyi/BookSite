from django.core.urlresolvers import reverse
from slugify import slugify


def image_directory_path(instance, filename):
    ext = ''
    if '.' in filename:
        filename, ext = filename.rsplit('.', 1)
    if hasattr(instance, 'image_path') and instance.image_path:
        image_path = instance.image_path
    else:
        image_path = instance.__class__.__name__.lower()

    if hasattr(instance, 'name') and instance.name:
        name = '{}_'.format(instance.name)
    elif hasattr(instance, 'value') and instance.value:
        name = '{}_'.format(instance.value)
    else:
        name = '{}_'.format(instance.pk)
    return 'images/{}/{}{}.{}'.format(
        image_path, slugify(name), slugify(filename), ext)
