from django.conf import settings
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from search.views import SearchView
from webshop.models import Product


class SearchPageTest(TestCase):
    fixtures = ['test.json']

    def get_num_pages(self):
        products = Product.objects.filter(name__icontains=self.query)
        # count_products = products.count()

        paginator = Paginator(products, settings.PRODUCT_ON_PAGE, orphans=3)

        page = paginator.num_pages

        return page

    def setUp(self):
        self.factory = RequestFactory()
        self.query = 'white'
        self.not_find_string = 'По запросу <strong>"{}"</strong> ничего не найдено.'

    def test_result_counts(self):
        request = self.factory.get(settings.LOGIN_REDIRECT_URL)
        response = SearchView.as_view()(request)
        print(response)
        print(SearchView.get_queryset(Product.objects.first()))

    def test_search_without_q(self):
        response = self.client.get(reverse('search:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.not_find_string.format(''))

    def test_search_with_empty_q(self):
        response = self.client.get(reverse('search:search'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.not_find_string.format(''))

    def test_search_with_q_len_1(self):
        q = 'w'
        response = self.client.get(reverse('search:search'), {'q': q})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.not_find_string.format(q))

    def test_search_with_q_len_2(self):
        q = 'wh'
        response = self.client.get(reverse('search:search'), {'q': q})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.not_find_string.format(q))

    def test_search_with_q_len_3(self):
        q = 'whi'
        response = self.client.get(reverse('search:search'), {'q': q})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.not_find_string.format(q))

    def test_search_with_q(self):
        response = self.client.get(reverse('search:search'), {'q': self.query})
        self.assertEqual(response.status_code, 200)

    def test_search_with_first_page(self):
        last_page = self.get_num_pages()
        page = 1
        response = self.client.get(reverse('search:search'), {'q': self.query, 'page': page})
        self.assertContains(response, 'Page {} of {}'.format(page, last_page))
        self.assertContains(response, '<a href="?q={}&page={}">next</a>'.format(self.query, page + 1))
        self.assertNotContains(response, '<a href="?q={}&page={}">previous</a>'.format(self.query, page - 1))

    def test_search_without_page(self):
        last_page = self.get_num_pages()
        page = 1
        response = self.client.get(reverse('search:search'), {'q': self.query})
        self.assertContains(response, 'Page {} of {}'.format(page, last_page))
        self.assertContains(response, '<a href="?q={}&page={}">next</a>'.format(self.query, page + 1))
        self.assertNotContains(response, '<a href="?q={}&page={}">previous</a>'.format(self.query, page - 1))

    def test_search_with_last_page(self):
        page = self.get_num_pages()

        response = self.client.get(reverse('search:search'), {'q': self.query, 'page': page})

        self.assertContains(response, 'Page {} of {}'.format(page, page))
        self.assertNotContains(response, '<a href="?q={}&page={}">next</a>'.format(self.query, page + 1))
        self.assertContains(response, '<a href="?q={}&page={}">previous</a>'.format(self.query, page - 1))
