from django import template
from ..models import Blog

register = template.Library()


@register.simple_tag()
def get_blogs():
    return Blog.objects.order_by('-create')[:3]