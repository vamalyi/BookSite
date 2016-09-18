from django.contrib.sitemaps import Sitemap
from django.db.models import Q

from webshop.models import Product, Category, PreFilter
from news.models import Post
from website.models import StaticPage


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class PrefilterSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return PreFilter.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class HomePageSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return StaticPage.objects.filter(url='index')

    def location(self, obj):
        return obj.get_absolute_url()


class StaticPageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.4

    def items(self):
        return StaticPage.objects.exclude(Q(url='index') | Q(url='thanks_order') | Q(url='comment_rules'))

    def location(self, obj):
        return obj.get_absolute_url()


class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.4

    def items(self):
        return Post.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()
