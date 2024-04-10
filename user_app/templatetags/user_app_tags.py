from django import template
from ..models import Blog, Department, CategoryBlog

register = template.Library()


@register.simple_tag()
def get_blogs():
    """
    Retrieves the latest three blogs from the 'Novini' category.

    Returns:
        QuerySet: Latest three blogs from the 'Novini' category, ordered by
    creation date.
    """
    return Blog.objects.filter(category__slug='novini').order_by('-create')[:3]


@register.simple_tag()
def get_departments_for_menu():
    """
    Retrieves all departments for the menu.

    Returns:
        QuerySet: All departments ordered by their numbers, with only
    'id' and 'name' fields included.
    """
    return Department.objects.all().order_by('number').values('id', 'name')


@register.simple_tag()
def get_blog_category_for_menu():
    """
    Retrieves all blog categories for the menu.

    Returns:
        QuerySet: All blog categories ordered by their IDs, with only
    'title' and 'slug' fields included.
    """
    return CategoryBlog.objects.all().order_by('id').values('title', 'slug')
