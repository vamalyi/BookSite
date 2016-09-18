from collections import defaultdict

from decimal import Decimal

from django.contrib import messages
from django.db import models
from django.db.models import Count, Q, F, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from frankie_web_platform import settings
from webshop.models import ProductParameterAvailableValue, Sale, ParameterRange
from webshop.models import Product, PreFilter, Category, ProductTreeReview
from webshop.forms import ProductReviewForm, ProductShortReviewForm
from webshop.signals import product_viewed
from website.models import GlobalSettings


class ProductView(DetailView):
    model = Product
    template_name = 'catalogue/product.html'
    context_object_name = 'product'
    slug_field = 'url'
    slug_url_kwarg = 'url'

    def get_queryset(self):
        products = super().get_queryset()

        return products.select_related('sale', 'margin', 'category', 'special_proposition',
                                       'provider').prefetch_related(
            'images', 'parameter_values__product_parameter', 'parameter_values__value', 'price_correctors')

    def get_similar_products(self, scope, count):
        price_from = self.object.default_price * scope[0]
        price_to = self.object.default_price * scope[1]

        products = Product.objects.filter(
            category=self.object.category, active=True, default_price__range=(price_from, price_to))
        products = products.select_related('category', 'provider', 'sale', 'margin', 'special_proposition')
        products = products.prefetch_related(
            'parameter_values', 'parameter_values__product_parameter', 'parameter_values__value',
            'price_correctors', 'images')
        products = products.exclude(id=self.object.id).order_by('?')[:count]
        return products

    def get(self, request, *args, **kwargs):
        self.global_settings = GlobalSettings.objects.first()

        response = super().get(request, *args, **kwargs)
        product_viewed.send(sender=self, product=self.object, user=request.user, request=request, response=response)
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx_update = {
            'seo': self.get_seo(),
            'similar_products': self.get_similar_products((Decimal('0.70'), Decimal('1.30')), 4),
            'series_products': Product.objects.filter(
                series__isnull=False, series=self.object.series).exclude(
                pk=self.object.id).order_by('?'), # 2_part, was slice [:4] at the end
        }
        if not self.request.user.is_authenticated():
            ctx_update['review_form'] = ProductReviewForm(product=self.object)
            ctx_update['review_short_form'] = ProductShortReviewForm(product=self.object)
        else:
            ctx_update['review_form'] = ProductReviewForm(product=self.object, user=self.request.user)
            ctx_update['review_short_form'] = ProductShortReviewForm(product=self.object, user=self.request.user)
        ctx.update(ctx_update)

        return ctx

    def get_meta_tag(self, tag):
        tag = tag.replace('<page_name>', '')
        tag = tag.replace('<company>',
                          self.global_settings.company_name if self.global_settings else '')
        tag = tag.replace('<product>', self.object.name)
        return tag.replace('<category>', self.object.category.name)

    def get_seo(self):
        if self.global_settings:
            title = self.get_meta_tag(self.global_settings.product_title)
            description = self.get_meta_tag(self.global_settings.product_description)
            keywords = self.get_meta_tag(self.global_settings.product_keywords)
        else:
            title = ''
            description = ''
            keywords = ''

        seo = {
            'title': self.object.meta_title or title,
            'meta_description': self.object.meta_description or description,
            'meta_canonical': self.object.meta_canonical,
            'meta_keywords': self.object.meta_keywords or keywords,
            'meta_robots': self.object.meta_robots,
            'h1': self.object.h1,
        }
        return seo


class CategoryView(ListView):
    model = Product
    template_name = 'catalogue/category.html'
    paginate_by = settings.PRODUCT_ON_PAGE
    context_object_name = 'products'
    

    price = {}
    params = {}
    category = None
    prefilter = None
    prefilter_params = None
    products_parameters = dict()
    all_products = list()
    

    def get_seo(self):
        if self.global_settings:
            title = self.get_meta_tag(self.global_settings.category_title)
            description = self.get_meta_tag(self.global_settings.category_description)
            keywords = self.get_meta_tag(self.global_settings.category_keywords)
        else:
            title = ''
            description = ''
            keywords = ''

        if self.prefilter:
            return {
                'title': self.prefilter.meta_title or self.category.meta_title or title,
                'meta_description': self.prefilter.meta_description or self.category.meta_description or description,
                'meta_canonical': self.prefilter.meta_canonical or self.category.meta_canonical,
                'meta_keywords': keywords,
                'meta_robots': self.prefilter.meta_robots or self.category.meta_robots,
                'h1': self.prefilter.h1 or self.category.h1,
            }
        return {
            'title': self.category.meta_title or title,
            'meta_description': self.category.meta_description or description,
            'meta_canonical': self.category.meta_canonical,
            'meta_keywords': keywords,
            'meta_robots': self.category.meta_robots,
            'h1': self.category.h1,
        }

    @staticmethod
    def get_params(params):
        prefilter_params = defaultdict(list)
        _params = params.split('?')
        if len(_params) in (1, 2):
            _params = _params[-1]
        else:
            _params = ''
        _params = _params.split('&')
        for p in _params:
            p = p.split('=')
            if len(p) != 2:
                raise ValueError(_('URL error.'))
            if p[1] and p[0] not in ('price_from', 'price_to', 'order', 'page'):
                prefilter_params[p[0]].append(p[1])
        # for k in self.params.keys():
        #     if k in prefilter_params.keys():
        #         for v in self.params[k]:
        #             if v not in prefilter_params[k]:
        #                 prefilter_params[k].append(v)
        #     else:
        #         prefilter_params[k] = self.params[k]
        return prefilter_params

    def get_prefilter_parameters(self):
        prefilter_params = defaultdict(list)
        if self.prefilter_params:
            prefilter_params = self.get_params(self.prefilter_params)
        return prefilter_params

    def set_params(self, request):
        self.params = dict(request.GET)

        try:
            self.price['from'] = min(map(float, self.params.pop('price_from')))
        except Exception:
            self.price['from'] = None
        try:
            self.price['to'] = max(map(float, self.params.pop('price_to')))
        except Exception:
            self.price['to'] = None
        
        self.ordering = self.params.pop('order', ['weight'])
        if self.ordering[0] == "price_ASC":
            self.ordering = ("default_price_sm", "default_price_s", "default_price_m", "default_price_c",
                             "default_price", "asc")
        elif self.ordering[0] == "price_DESC":
            self.ordering = ("default_price_sm", "default_price_s", "default_price_m", "default_price_c",
                             "default_price", "desc")
        elif self.ordering[0] == "date_ASC":
            self.ordering = "-date_on_add"
        elif self.ordering[0] == "date_DESC":
            self.ordering = "date_on_add"
        elif self.ordering[0] == "name_ASC":
            self.ordering = "name"
        elif self.ordering[0] == "name_DESC":
            self.ordering = "-name"
        else:
            self.ordering = self.ordering[0]
        
        prefilter_params = self.get_prefilter_parameters()

        if self.prefilter_params:
            self.params = dict(prefilter_params)

        self.page = self.params.pop('page', 1)

        self.params = dict([(k, self.params[k]) for k in self.params.keys() if k.isdigit()])

    def get(self, request, *args, **kwargs):
        self.global_settings = GlobalSettings.objects.first()
        self.prefilter = None
        self.prefilter_params = None
        self.products_parameters = dict()

        prefilter = kwargs.get('prefilter')
        category = kwargs.get('category')
        if prefilter:
            self.prefilter = get_object_or_404(PreFilter, url='{}/{}'.format(category, prefilter))
            self.prefilter_params = self.prefilter.original_url
        self.category = get_object_or_404(Category, url=category)
        self.set_params(request)

        if not prefilter:
            prefilters = list(PreFilter.objects.values('id', 'original_url'))
            prefilters = [(p['id'], self.get_params(p['original_url'])) for p in prefilters]
            if self.params:
                for prefilter_id, prefilter_params in prefilters:
                    prefilter_order = dict([(k, set(prefilter_params[k])) for k in prefilter_params.keys()])
                    params_order = dict([(k, set(self.params[k])) for k in self.params.keys()])
                    if prefilter_order == params_order:
                        params = []
                        if self.price['from'] and self.price['from'] > 0:
                            params.append('price_from={}'.format(int(self.price['from'])))
                        if self.price['to'] and self.price['to'] > 0:
                            params.append('price_to={}'.format(int(self.price['to'])))
                        if self.ordering and self.ordering != 'weight':
                            params.append('order={}'.format(self.get_url_order()))
                        url = '/catalogue/{}'.format(PreFilter.objects.get(pk=prefilter_id).url)
                        if params:
                            url = '{}/?{}'.format(url, '&'.join(params))
                        return HttpResponseRedirect(url)

        return super().get(request, *args, **kwargs)

    @staticmethod
    def get_parameter_ids(params):
        keys = params.keys()
        parameter_ids = {'values': [], 'ranges': []}
        for key in keys:
            parameter_range = ParameterRange.objects.filter(parameter=key).prefetch_related('available_values')
            for parameter in params[key]:
                if parameter_range.exists():
                    parameter_ids['ranges'].append(str(parameter))
                else:
                    parameter_ids['values'].append(str(parameter))
        return parameter_ids

    @staticmethod
    def get_parameter_ids_with_range(params):
        keys = params.keys()
        parameter_ids = list()
        for key in keys:
            parameter_range = ParameterRange.objects.filter(parameter=key).prefetch_related('available_values')
            for parameter in params[key]:
                if parameter_range.exists():
                    for val in parameter_range.get(pk=parameter).available_values.values_list('id', flat=True):
                        parameter_ids.append(val)
                else:
                    parameter_ids.append(str(parameter))
        return parameter_ids

    def create_product_parameters(self, products):
        if self.price['from'] or self.price['to']:
            products = self.filter_prices(products.select_related('provider', 'sale', 'margin'))
        for k in self.params.keys():
            params_copy = self.params.copy()
            del params_copy[k]
            num = len(params_copy)
            val = self.get_parameter_ids_with_range(params_copy)
            if val:
                self.products_parameters[k] = products.filter(parameter_values__value__in=val)
            else:
                self.products_parameters[k] = products
            self.products_parameters[k] = self.products_parameters[k].annotate(
                values_count=Count('parameter_values__value'),
                params_count=Count('parameter_values__product_parameter')).filter(
                values_count__gte=num, params_count__gte=num).order_by()

    def append_values_to_parameter_values(self, values_list, ids=[]):
        values_list = values_list.annotate(value_count=Count('parameter_values__product'))
        values_list = values_list.filter(Q(value_count__gt=0))
        values_list = values_list.order_by('product_parameter__weight', 'weight')
        for value_item in list(values_list.values(
                'product_parameter__name', 'product_parameter__weight',
                'product_parameter', 'value', 'weight', 'id', 'value_count',
        )):
            value_item['type'] = 'values'
            if str(value_item['id']) in ids:
                value_item['checked'] = True
                value_item['plus'] = False
            else:
                value_item['checked'] = False
                if ids:
                    value_item['plus'] = True
            self.parameter_values.append(value_item)

    def append_ranges_to_parameter_values(self, ranges_list, ids=[]):
        ranges_list = ranges_list.annotate(value_count=Count('available_values__parameter_values__product'))
        ranges_list = ranges_list.filter(Q(value_count__gt=0))
        ranges_list = ranges_list.order_by('parameter__weight', 'weight')
        for range_item in list(ranges_list.values(
                'parameter__name', 'parameter__weight', 'parameter', 'name', 'weight', 'id', 'value_count',
        )):
            if str(range_item['id']) in ids:
                range_item['checked'] = True
                range_item['plus'] = False
            else:
                range_item['checked'] = False
                if ids:
                    range_item['plus'] = True
            self.parameter_values.append({
                'product_parameter__name': range_item['parameter__name'],
                'product_parameter__weight': range_item['parameter__weight'],
                'product_parameter': range_item['parameter'],
                'value': range_item['name'],
                'weight': range_item['weight'],
                'id': range_item['id'],
                'value_count': range_item['value_count'],
                'checked': range_item['checked'],
                'type': 'ranges',
                'plus': range_item['plus']
            })

    def append_empty_selected_values(self, ids):
        ii = [str(i['id']) for i in self.parameter_values if i['type'] == 'values']
        for v_id in ids['values']:
            if v_id not in ii:
                value = ProductParameterAvailableValue.objects.get(pk=v_id)
                self.parameter_values.append({
                    'product_parameter__name': value.product_parameter.name,
                    'product_parameter__weight': value.product_parameter.weight,
                    'product_parameter': value.product_parameter_id,
                    'value': value.value,
                    'weight': value.weight,
                    'id': v_id,
                    'value_count': 0,
                    'checked': True,
                    'type': 'values',
                })

        ii = [str(i['id']) for i in self.parameter_values if i['type'] == 'ranges']
        for r_id in ids['ranges']:
            if r_id not in ii:
                range_item = ParameterRange.objects.get(pk=r_id)
                self.parameter_values.append({
                    'product_parameter__name': range_item.parameter.name,
                    'product_parameter__weight': range_item.parameter.weight,
                    'product_parameter': range_item.parameter_id,
                    'value': range_item.name,
                    'weight': range_item.weight,
                    'id': r_id,
                    'value_count': 0,
                    'checked': True,
                    'type': 'values',
                })

    def create_parameter_attribute_values(self, products):
        self.parameter_values = list()
        ids = self.get_parameter_ids(self.params)
        for k in self.products_parameters.keys():
            parameter_range = ParameterRange.objects.filter(parameter=k).prefetch_related('available_values')
            if parameter_range.exists():
                ranges_list = ParameterRange.objects.filter(
                    Q(parameter=k) & Q(available_values__parameter_values__product__in=self.products_parameters[k]))
                self.append_ranges_to_parameter_values(ranges_list, ids['ranges'])
            else:
                values_list = ProductParameterAvailableValue.objects.filter(
                    Q(parameter_values__product__in=self.products_parameters[k]) & Q(product_parameter=k))
                self.append_values_to_parameter_values(values_list, ids['values'])

        values_list = ProductParameterAvailableValue.objects.filter(
            parameter_values__product__in=products, product_parameter__ranges__isnull=True).exclude(
            product_parameter__in=self.params.keys())
        self.append_values_to_parameter_values(values_list)

        ranges_list = ParameterRange.objects.filter(
            available_values__parameter_values__product__in=products).exclude(parameter__in=self.params.keys())
        self.append_ranges_to_parameter_values(ranges_list)

        self.append_empty_selected_values(ids)

    def filter_prices(self, products, filter=True):
        products = products.annotate(
            # default_price_sm=F('default_price') * F('provider__coefficient') * (100 - F('sale__percent') / 100) *
            #                  (100 - F('margin__percent') / 100),
            # default_price_s=F('default_price') * F('provider__coefficient') * (100 - F('sale__percent') / 100),
            # default_price_m=F('default_price') * F('provider__coefficient') * (100 - F('margin__percent') / 100),
            # default_price_c=F('default_price') * F('provider__coefficient')
            default_price_sm=ExpressionWrapper(
                F('default_price') * F('provider__coefficient') * (1 - F('sale__percent') / 100) *
                (1 - F('margin__percent') / 100),
                output_field=models.DecimalField(decimal_places=2, max_digits=12)
            ),
            default_price_s=ExpressionWrapper(
                F('default_price') * F('provider__coefficient') * (1 - F('sale__percent') / 100),
                output_field=models.DecimalField(decimal_places=2, max_digits=12)
            ),
            default_price_m=ExpressionWrapper(
                F('default_price') * F('provider__coefficient') * (1 - F('margin__percent') / 100),
                output_field=models.DecimalField(decimal_places=2, max_digits=12)
            ),
            default_price_c=ExpressionWrapper(
                F('default_price') * F('provider__coefficient'),
                output_field=models.DecimalField(decimal_places=2, max_digits=12)
            )
        )

        if filter:
            price_from, price_to = self.price['from'], self.price['to']
            if price_from and price_to:
                price_from = Decimal(price_from)
                price_to = Decimal(price_to)
                products = products.filter(
                    Q(default_price_c__range=(price_from, price_to), default_price_s__isnull=True,
                      default_price_m__isnull=True) |
                    Q(default_price_m__range=(price_from, price_to), default_price_sm__isnull=True,
                      default_price_s__isnull=True) |
                    Q(default_price_s__range=(price_from, price_to), default_price_sm__isnull=True,
                      default_price_m__isnull=True) |
                    Q(default_price_sm__range=(price_from, price_to))
                )
            elif price_from:
                price_from = Decimal(price_from)
                products = products.filter(
                    Q(default_price_c__gte=price_from, default_price_s__isnull=True,
                      default_price_m__isnull=True) |
                    Q(default_price_m__gte=price_from, default_price_sm__isnull=True,
                      default_price_s__isnull=True) |
                    Q(default_price_s__gte=price_from, default_price_sm__isnull=True,
                      default_price_m__isnull=True) |
                    Q(default_price_sm__gte=price_from)
                )
            elif price_to:
                price_to = Decimal(price_to)
                products = products.filter(
                    Q(default_price_c__lte=price_to, default_price_s__isnull=True,
                      default_price_m__isnull=True) |
                    Q(default_price_m__lte=price_to, default_price_sm__isnull=True,
                      default_price_s__isnull=True) |
                    Q(default_price_s__lte=price_to, default_price_sm__isnull=True,
                      default_price_m__isnull=True) |
                    Q(default_price_sm__lte=price_to)
                )
        return products

    def get_url_order(self):
        ordering = self.get_ordering()
       
        if ordering == 'date_on_add':
            ordering = 'date_DESC'
        elif ordering == '-date_on_add':
            ordering = 'date_ASC'
        elif ordering == '-default_price_sm':
            ordering = 'price_DESC'
        elif ordering == 'default_price_sm':
            ordering = 'price_ASC'
        elif self.ordering[0] == "name":
            self.ordering = "name_ASC"
        elif self.ordering[0] == "-name":
            self.ordering = "name_DESC"
        return ordering

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
        print(type(self.ordering))
        if type(self.ordering) == tuple:
            if self.ordering[-1] == 'asc':
                products = products.order_by(Coalesce(*self.ordering[:-1]).asc())
            else:
                products = products.order_by(Coalesce(*self.ordering[:-1]).desc())
        elif self.ordering == 'weight':                     # 3_part, added
            products = products.order_by('series', 'name')  # 3_part, added
        else:
            products = products.order_by(self.ordering)
        
        return products

    def filter_params(self, products):
        if len(self.params):
            self.create_product_parameters(self.params_products)

            num = len(self.params)
            val = self.get_parameter_ids_with_range(self.params)
            products = products.filter(parameter_values__value__in=val).annotate(
                values_count=Count('parameter_values__value'),
                params_count=Count('parameter_values__product_parameter')).filter(
                values_count__gte=num, params_count__gte=num).order_by()
        return products

    def get_queryset(self):
        products = super().get_queryset().filter(active=True, category=self.category)

        self.params_products = products.prefetch_related(
            'parameter_values__product_parameter', 'parameter_values__value',
        )

        products = products.select_related(
            'provider', 'sale', 'margin').prefetch_related(
            'parameter_values__product_parameter', 'parameter_values__value',
        )

        # self.products_without_price_filter = self.filter_params(self.filter_prices(products, False))
        products = self.filter_prices(products)
        products = self.filter_params(products)
        self.all_products = products
        products = products.select_related(
            'category', 'special_proposition').prefetch_related(
            'price_correctors', 'images')

        products = self.order_products(products)

        return products

    def get_paginate_by(self, queryset):
        product_on_page = self.request.COOKIES.get('product_on_page', self.paginate_by)
        if product_on_page == 'all':
            return self.object_list.count()
        return product_on_page

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        self.create_parameter_attribute_values(self.all_products)
        # prices = list()
        # for i in self.all_products.values_list(
        #         'default_price_sm', 'default_price_s', 'default_price_m', 'default_price_c'):
        #     if i[0]:
        #         prices.append(i[0])
        #     elif i[1]:
        #         prices.append(i[1])
        #     elif i[2]:
        #         prices.append(i[2])
        #     elif i[3]:
        #         prices.append(i[3])
        # if prices:
        #     min_max = (min(prices), max(prices))
        # else:
        #     min_max = (0, 0)
        # prices = list()
        # for i in self.products_without_price_filter.values_list(
        #         'default_price_sm', 'default_price_s', 'default_price_m', 'default_price_c'):
        #     if i[0]:
        #         prices.append(i[0])
        #     elif i[1]:
        #         prices.append(i[1])
        #     elif i[2]:
        #         prices.append(i[2])
        #     elif i[3]:
        #         prices.append(i[3])
        # if prices:
        #     price_max = max(prices)
        # else: price_max = 0

        ctx_update = {
            'category': self.category,
            'seo': self.get_seo(),
            'prefilter_from_catagory': {'prefilters': PreFilter.objects.filter(
                active=True, url__contains=self.kwargs.get('category')).all(), 'url': self.request.path},

            # 'price_min': self.price['from'] or int(min_max[0]),
            # 'price_max': self.price['to'] or int(min_max[1]) + 1,
            # 'price_max_all': int(price_max) + 1,

            'order': self.get_ordering(),
            'price_from': self.price['from'] or '',
            'price_to': self.price['to'] or '',
            'filter_get': self.request.GET.urlencode(),
            'filters': self.parameter_values,
            'product_on_page': self.request.COOKIES.get('product_on_page', self.paginate_by),
            'prefilter': self.prefilter,
            'products_count': ctx['paginator'].count,
            'all_products_count': Product.objects.filter(category=self.category, active=True).count(),
            'is_params': bool(self.params),
        }

        ctx.update(ctx_update)

        return ctx

    def get_meta_tag(self, tag):
        tag = tag.replace('<page_name>', '')
        tag = tag.replace('<company>',
                          self.global_settings.company_name if self.global_settings else '')
        tag = tag.replace('<product>', '')
        return tag.replace('<category>', self.category.name)


class NoveltyListView(ListView):
    model = Product
    template_name = 'catalogue/novelty.html'
    paginate_by = settings.PRODUCT_ON_PAGE
    context_object_name = 'products'

    def get_queryset(self):
        # return super().get_queryset().filter(special_proposition__name='new')
        return super().get_queryset().filter(is_new=True)

    def get_paginate_by(self, queryset):
        product_on_page = self.request.COOKIES.get('product_on_page', self.paginate_by)
        if product_on_page == 'all':
            return self.object_list.count()
        return product_on_page

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['product_on_page'] = self.request.COOKIES.get('product_on_page', self.paginate_by)

        return ctx


class SetProductSale(TemplateView):
    model = Product
    template_name = 'admin/product/set_sale.html'

    def get(self, request, *args, **kwargs):
        if not (request.user.is_authenticated() and request.user.has_perm('webshop.change_product')):
            return HttpResponseRedirect('/admin/')
        self.pks = kwargs.get('pks', '')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['pks'] = self.pks
        ctx['sales'] = Sale.objects.all()
        ctx['products'] = self.model.objects.filter(id__in=self.pks.split(','))

        return ctx

    def post(self, request, *args, **kwargs):
        if not (request.user.is_authenticated() and request.user.has_perm('webshop.change_product')):
            return HttpResponseRedirect('/admin/')
        post = request.POST
        pks = post.get('pks').split(',')
        sale = post.get('sale')
        self.model.objects.filter(id__in=pks).update(sale_id=sale)
        return HttpResponseRedirect('/admin/webshop/product/')


class CreateReviewView(CreateView):
    model = ProductTreeReview
    form_class = ProductReviewForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if settings.MODERATE_REVIEWS and not self.request.user.is_staff:
            messages.success(self.request, 'Ваш отзыв принят на модерацию, после проверки он появится на сайте.')

        return response

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, url=kwargs['url'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.product.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product'] = self.product
        kwargs['user'] = self.request.user
        return kwargs


class CreateShortReviewView(CreateView):
    model = ProductTreeReview
    form_class = ProductShortReviewForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if settings.MODERATE_REVIEWS and not self.request.user.is_staff:
            if self.object.level == 0:
                messages.success(self.request, 'Ваш вопрос принят на модерацию, после проверки он появится на сайте.')
            else:
                messages.success(self.request, 'Ваш ответ принят на модерацию, после проверки он появится на сайте.')

        return response

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, url=kwargs['url'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.product.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product'] = self.product
        kwargs['user'] = self.request.user
        return kwargs
