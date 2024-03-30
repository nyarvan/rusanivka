from django import template
from ..models import Blog, Department, CategoryBlog

register = template.Library()


@register.simple_tag()
def get_blogs():
    return Blog.objects.filter(category__slug='novini').order_by('-create')[:3]


@register.simple_tag()
def get_departments_for_menu():
    return Department.objects.all().order_by('number').values('id', 'name')


@register.simple_tag()
def get_blog_category_for_menu():
    return CategoryBlog.objects.filter().order_by('id').values('title', 'slug')
