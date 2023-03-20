from django import template
from ..models import Blog, Department

register = template.Library()


@register.simple_tag()
def get_blogs():
    return Blog.objects.order_by('-create')[:3]


@register.simple_tag()
def get_departments_for_menu():
    return Department.objects.all().order_by('number').values('id', 'name')
