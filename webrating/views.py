from django.shortcuts import render

from django.http import Http404

import website.models as wsm
import webrating.models as wrm
import webform.forms as wff


def comments(request):
    try:
        # Static Page:
        static_page_all = wsm.StaticPage.objects.all()
        comments_page = static_page_all.filter(url='comments').first()

        # SEO attributes:
        seo = {
            'title': comments_page.meta_title,
            'meta_description': comments_page.meta_description,
            'meta_canonical': comments_page.meta_canonical,
            'meta_robots': comments_page.meta_robots,
            'h1': comments_page.h1,
        }

        # Galleries:
        gallery = None
        if comments_page.gallery:
            gallery = wsm.GalleryImagePosition.objects.filter(gallery=wsm.Gallery.objects.filter(
                name=comments_page.gallery.name).first()).all()

        # Banners:
        all_banners = wsm.Banner.objects.all()
        image_positions = wsm.Banners()
        if all_banners:
            for banner in all_banners:
                image_position = wsm.BannerImagePosition.objects.filter(banner=wsm.Banner.objects.filter(
                    name=banner.name).first()).all()
                image_positions.append(banner.name, image_position)

        # Ratings and comments:
        ratings = wrm.Rating.objects.order_by('date_on_add').all()
        if request.POST and request.POST['comment_add']:
            result, form = wff.FormRatingGlobal.process(request)
        else:
            form = wff.FormRatingGlobal()

        # Bread crumbs
        bread_crumbs = [
            {
                'url': '/',
                'name': static_page_all.filter(url='index').first().name
            },
            {
                'url': '',
                'name': comments_page.name
            },
        ]

        return render(request, 'static_comments.html', {
            'seo': seo,
            'static_comments': comments_page,
            'banners': image_positions,
            'gallery': gallery,
            'bread_crumbs': bread_crumbs,
            'ratings': ratings,
            'form_rating': form,
            # 'cart_preview': get_products_in_cart(request),
        })
    except:
        raise Http404('Page not found')
