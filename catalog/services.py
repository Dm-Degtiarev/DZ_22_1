from django.conf import settings
from django.core.cache import cache
from catalog.models import Category


def get_cache_categories():
    queryset = Category.objects.all()
    if settings.CACHE_ENABLE:
        key = 'categories_cache'
        cache_category = cache.get(key)
        if cache_category is None:
            cache_category = queryset
            cache.set(key, cache_category)
        return cache_category
    return queryset