from django.contrib import sitemaps
from user_app.models import Department, Blog


class AbstractSitemapClass:
    changefreq = 'daily'
    url = None

    def get_absolute_url(self):
        return self.url


class StaticViewSitemap(sitemaps.Sitemap):
    pages = {
        'home_view': '/',
        'admin_view': '/administration/',
        'blogs_view': '/blog/news/',
        'contact_view': '/contact/'
    }

    main_sitemaps = []
    for page in pages.keys():
        sitemap_class = AbstractSitemapClass()
        sitemap_class.url = pages[page]
        main_sitemaps.append(sitemap_class)

    def items(self):
        return self.main_sitemaps

    priority = 1
    changefreq = 'daily'


class DepartmentSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Department.objects.all()


class BlogSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created
        