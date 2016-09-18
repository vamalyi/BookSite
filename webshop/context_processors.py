from webshop.models import FastSearch


def fast_search(request):
    fast_search_words = FastSearch.published.values_list('value', flat=True)
    return {'fast_search_words': fast_search_words}
