from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

import website.models as wsm
from news.models import Post
from webform.forms import send_email
from website.models import StaticPage
from webshop.models import Product


class StaticPageView(TemplateView):
    template_name = 'static/page.html'

    def get(self, request, *args, **kwargs):
        if self.args[0] == 'index':
            raise Http404
        self.object = get_object_or_404(StaticPage, url=self.args[0])
        self.global_settings = wsm.GlobalSettings.objects.first()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['static_page'] = self.object
        ctx['seo'] = self.get_seo()

        return ctx

    def get_meta_tag(self, tag):
        tag = tag.replace('<page_name>', self.object.name)
        tag = tag.replace('<company>',
                          self.global_settings.company_name if self.global_settings else '')
        tag = tag.replace('<product>', '')
        return tag.replace('<category>', '')

    def get_seo(self):
        if self.global_settings:
            title = self.get_meta_tag(self.global_settings.static_page_title)
            description = self.get_meta_tag(self.global_settings.static_page_description)
            keywords = self.get_meta_tag(self.global_settings.static_page_keywords)
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
        }
        return seo


class HomePageView(TemplateView):
    template_name = 'static/index.html'

    def get(self, request, *args, **kwargs):
        self.object = StaticPage.objects.filter(url='index')
        self.global_settings = wsm.GlobalSettings.objects.first()

        return super().get(request, *args, **kwargs)

    def get_meta_tag(self, tag):
        page_name = self.object.get().name if self.object.exists() else _('Home page')
        tag = tag.replace('<page_name>', str(page_name))
        tag = tag.replace('<company>',
                          self.global_settings.company_name if self.global_settings else '')
        tag = tag.replace('<product>', '')
        return tag.replace('<category>', '')

    def get_seo(self):
        if self.global_settings:
            title = self.get_meta_tag(self.global_settings.static_page_title)
            description = self.get_meta_tag(self.global_settings.static_page_description)
            keywords = self.get_meta_tag(self.global_settings.static_page_keywords)
        else:
            title = ''
            description = ''
            keywords = ''

        object_title = self.object.get().meta_title if self.object.exists() else None
        object_description = self.object.get().meta_description if self.object.exists() else None
        object_meta_canonical = self.object.get().meta_canonical if self.object.exists() else ''
        object_meta_robots = self.object.get().meta_robots if self.object.exists() else ''
        object_meta_keywords = self.object.get().meta_keywords if self.object.exists() else None
        seo = {
            'title': object_title or title,
            'meta_description': object_description or description,
            'meta_canonical': object_meta_canonical,
            'meta_keywords': object_meta_keywords or keywords,
            'meta_robots': object_meta_robots,
        }
        return seo

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['seo'] = self.get_seo()

        products = Product.objects.filter(active=True).select_related(
            'category', 'provider', 'sale', 'margin', 'special_proposition').prefetch_related(
            'parameter_values', 'parameter_values__product_parameter', 'parameter_values__value',
            'price_correctors', 'images')

        sale_products = products.filter(sale__isnull=False)
        top_products = products.filter(is_top=True)
        hit_products = products.filter(is_hit=True)
        new_products = products.filter(special_proposition__name='new')

        ctx_update = {
            'news': Post.objects.filter(type='NEWS', status='PUBLISHED').order_by('-created_date')[:4],
            'top_products': top_products,
            'hit_products': hit_products,
            'new_products': new_products,
            'sale_products': sale_products,
            'static_page': self.object.get() if self.object.exists() else '',
        }
        ctx.update(ctx_update)

        return ctx


def page(request, page_url):
    # Static Page:
    static_page_all = StaticPage.objects.all()
    static_page = static_page_all.filter(url=page_url).first()
    template = static_page.template.path

    # SEO attributes:
    seo = {
        'title': static_page.meta_title,
        'meta_description': static_page.meta_description,
        'meta_canonical': static_page.meta_canonical,
        'meta_robots': static_page.meta_robots,
        'h1': static_page.h1,
    }

    # Galleries:
    gallery = None
    if static_page.gallery:
        gallery = wsm.GalleryImagePosition.objects.order_by('weight').filter(gallery=static_page.gallery)

    # Banners:
    all_banners = wsm.Banner.objects.all()
    image_positions = wsm.Banners()
    if all_banners:
        for banner in all_banners:
            image_position = wsm.BannerImagePosition.objects.order_by('weight').filter(
                banner=wsm.Banner.objects.filter(name=banner.name).first(), active=True).all()
            image_positions.append(banner.name, image_position)

    # Bread crumbs
    bread_crumbs = []
    index_url = 'index'

    if static_page.url != index_url:
        bread_crumbs = [
            {
                'url': '/',
                'name': static_page_all.filter(url=index_url).first().name
            },
            {
                'url': '',
                'name': static_page.name
            },
        ]

    return render(request, template, {
        'seo': seo,
        'static_page': static_page,
        'banners': image_positions,
        'gallery': gallery,
        'bread_crumbs': bread_crumbs,
    })


def index_page(request):
    return page(request, 'index')


def callback(request):
    if request.method == 'GET':
        name = request.GET.get('name', None)
        phone = request.GET.get('phone', None)

        global_settings = wsm.GlobalSettings.objects.first()
        if global_settings:
            recipient_list = global_settings.emails.split(',')
            recipient_list = [mail.replace(' ', '') for mail in recipient_list]
            ctx = {
                'subject': _('Callback'),
                'message': '',
                'name': name,
                'phone': phone,
            }
            send_email(recipient_list, ctx, 'email/callback_admin.html')

            return HttpResponseRedirect(reverse('thanks_callback'))
    return HttpResponseRedirect('/')


class ThanksCallback(TemplateView):
    template_name = 'callback/thanks_callback.html'
