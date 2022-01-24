from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from user_app.models import Department, Doctor, Administration


class StaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return ['user_app:home_view', 'user_app:admin_view', 'user_app:ambulant_view', 'user_app:blogs_view',
                'user_app:blog_single_view', 'user_app:contact_view']

    def location(self, item):
        return reverse(item)


class DepartmentSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Department.objects.all()


class DoctorSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Doctor.objects.filter(is_visible=True)


class AdministrationSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Administration.objects.all()

