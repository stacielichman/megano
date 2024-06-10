from django import template
from django.urls import reverse

from shopapp.models import Banner, Categories

register = template.Library()


@register.simple_tag
def reference_to_products():
    return Categories.objects.filter(parent__isnull=True)


@register.simple_tag
def reference_to_big_banners():
    return Banner.objects.filter(is_big=True, is_active=True)


@register.simple_tag
def reference_to_small_banners():
    return Banner.objects.filter(is_big=False, is_active=True)
