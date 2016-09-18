import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.template.response import TemplateResponse
from jinja2 import Environment, FileSystemLoader
from jinja2 import Template

from webshop.models import Category, DeliveryRule, Product


def render_yml(request):
    # loader = FileSystemLoader(os.path.join(settings.BASE_DIR, 'templates'))
    # env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    # template = env.get_template('yandex.yml')

    data = {
        'shop_name': 'Mona.com.ua',
        'shop_url': '{}://{}'.format(request.META.get('wsgi.url_scheme', 'http'), request.META.get('HTTP_HOST')),
        'company_name': 'Mona company',
        'now_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'categories': Category.objects.all(),
        'deliveries': DeliveryRule.objects.all(),
        'products': Product.objects.select_related(
            'sale', 'margin', 'category', 'manufacturer').prefetch_related(
            'images', 'parameter_values__product_parameter', 'parameter_values__value')
    }

    content_type='application/xml'
    # template = Template('Hello {{ name }}!')
    # t = template.render(data)
    response = TemplateResponse(request, 'yandex.html', data,
                                content_type=content_type)
    return response
