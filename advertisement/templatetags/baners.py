import random

from django import template
from advertisement.models import Banner

register = template.Library()


@register.inclusion_tag('banners.html')
def get_banner():
    banners_list = list(Banner.objects.all())
    random.shuffle(banners_list)
    return {
        'banners': banners_list[:4]
    }
