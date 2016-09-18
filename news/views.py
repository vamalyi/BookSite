from django.conf import settings
from django.views.generic import ListView, DetailView

from news.models import Post
from website.models import GlobalSettings


class NewsListView(ListView):
    model = Post
    paginate_by = settings.NEWS_ON_PAGE
    content_object_name = 'news_list'
    context_object_name = 'news_list'
    template_name = 'news/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(status='PUBLISHED', type='NEWS')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        global_settings = GlobalSettings.objects.first()
        if global_settings:
            ctx_update = {
                'seo': {
                    'title': global_settings.news_title,
                    'meta_description': global_settings.news_description,
                    'meta_keywords': global_settings.news_keywords,
                },
            }

            ctx.update(ctx_update)

        return ctx


class NewsDetailView(DetailView):
    model = Post
    context_object_name = 'news'
    template_name = 'news/detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(status='PUBLISHED', type='NEWS')

    def get_template_names(self):
        template = self.object.template
        if template:
            return [template] + super().get_template_names()
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx_update = {
            'static_page': self.object,
        }

        ctx.update(ctx_update)

        return ctx
