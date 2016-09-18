from solid_i18n.urls import solid_i18n_patterns

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.generic.base import RedirectView

from frankie_web_platform import settings
from news.views import NewsListView, NewsDetailView

from website.views import HomePageView, StaticPageView, callback, ThanksCallback
from webshop.views import ProductView, CategoryView, SetProductSale, NoveltyListView, CreateReviewView, \
    CreateShortReviewView
import webshopcart.views
from search.views import SearchView, AuthorFilterView, SeriesFilterView
from search.views import ProductSearchByParameterValueView
from webshop.sitemap import (ProductSitemap, CategorySitemap, NewsSitemap, PrefilterSitemap, HomePageSitemap,
                             StaticPageSitemap)
from webshop.sitemap_yml import render_yml
from webshopcart import api


sitemaps = {
    'home': HomePageSitemap,
    'prefilter': PrefilterSitemap,
    'category': CategorySitemap,
    'posts': ProductSitemap,
    'news': NewsSitemap,
    'static_page': StaticPageSitemap,
}


def set_language(request, lang):
    path = request.path
    user_language = lang
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return HttpResponseRedirect(path)


def set_ru(request):
    return set_language(request, 'ru')


def set_uk(request):
    return set_language(request, 'uk')


def set_en(request):
    return set_language(request, 'en')


news_patterns = ([
    url(r'^$', NewsListView.as_view(), name='list'),
    url(r'^(?P<url>[-_\w]+)_(?P<pk>\d+)/$', NewsDetailView.as_view(), name='detail'),
], 'news')

search_patterns = ([
    url(r'^$', SearchView.as_view(), name='search'),
    # url(r'^author/$', AuthorListView.as_view(), name='author_list'),
    url(r'^author/(?P<mfa>[-_\w]+)/$', AuthorFilterView.as_view(),
        name='author_filter'),
    url(r'^series/(?P<mfa>[-_\w]+)/$', SeriesFilterView.as_view(),
        name='series_filter'),
    url(r'^parameter/$', ProductSearchByParameterValueView.as_view(), name='parameter'),
], 'search')

catalogue_patterns = ([
    url(r'^category/(?P<category>[-_\w]+)(/(?P<prefilter>[-_\w]+))*/$',
        CategoryView.as_view(), name='category_list'),
    url(r'^product/(?P<url>[-_\w]+)/$', ProductView.as_view(), name='product_detail'),
                          url(r'^product/(?P<url>[-_\w]+)/reviews/add/$', CreateReviewView.as_view(),
                              name='create_review'),
                          url(r'^product/(?P<url>[-_\w]+)/reviews/add_short/$', CreateShortReviewView.as_view(),
                              name='create_short_review'),
], 'catalogue')

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap\.yml$', render_yml),

    url(r'^admin/set_product_sale/(?P<pks>[,\d]+)/$', SetProductSale.as_view(), name='set_product_sale'),
]

main_urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home_page'),

    url(r'^search/', include(search_patterns, namespace='search')),
    url(r'^news/', include(news_patterns, namespace='news')),

    url(r'^novelty/$', NoveltyListView.as_view(), name='novelty_products'),

    url(r'^accounts/', include('webaccount.urls', namespace='account')),

    url(r'^basket/$', webshopcart.views.BasketView.as_view(), name='basket'),

    # catalogue
    url(r'^catalogue/', include(catalogue_patterns, namespace='catalogue')),

    url(r'^callback/$', callback, name='callback'),
    url(r'^thanks_callback/$', ThanksCallback.as_view(), name='thanks_callback'),

    url(r'^([-_\w]+)/$', StaticPageView.as_view(), name='page'),
]
if len(settings.LANGUAGES) > 1:
    urlpatterns += solid_i18n_patterns(*main_urlpatterns)
else:
    urlpatterns += main_urlpatterns

urlpatterns += [

    url(r'^api/cities/$', api.get_nova_poshta_cities),
    url(r'^api/warehouses/(?P<city>[-\w]+)/$', api.get_nova_poshta_warehouses),

    url(r'^api/add_product/$', api.add_product),
    url(r'^api/set_product/$', api.set_product),
    url(r'^api/del_product/$', api.del_product),

    # url(r'^ru/', set_ru, name='set_ru'),
    # url(r'^uk/', set_uk, name='set_uk'),
    # url(r'^en/', set_en, name='set_en'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
