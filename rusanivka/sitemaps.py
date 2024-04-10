from django.contrib import sitemaps
from user_app.models import Department, Blog


class AbstractSitemapClass:
    """
    Abstract base class for sitemap classes.

    This class defines common attributes and methods for sitemap classes.

    Attributes:
        changefreq (str): The change frequency of the URL. Defaults to 'daily'.
        url (str): The absolute URL of the resource.

    """

    changefreq = 'daily'
    url = None

    def get_absolute_url(self):
        """
        Method to get the absolute URL of the resource.

        Returns:
            str: The absolute URL of the resource.

        """

        return self.url


class StaticViewSitemap(sitemaps.Sitemap):
    """
    Sitemap class for static views.

    This class generates sitemap entries for static views.

    Attributes:
        pages (dict): A dictionary containing static view names and their URLs.
        main_sitemaps (list): A list containing instances of
        AbstractSitemapClass for each static view.

    """

    pages = {
        'home_view': '/',
        'admin_view': '/administration/',
        'blogs_view': '/blog/news/',
        'contact_view': '/contact/'
    }

    main_sitemaps = []
    for page, url in pages.items():
        sitemap_class = AbstractSitemapClass()
        sitemap_class.url = url
        main_sitemaps.append(sitemap_class)

    def items(self):
        """
        Method to return sitemap items.

        Returns:
            list: The list of sitemap items.

        """
        return self.main_sitemaps

    priority = 1
    changefreq = 'daily'


class DepartmentSitemap(sitemaps.Sitemap):
    """
    Sitemap class for Department model.

    This class generates sitemap entries for Department objects.

    Attributes:
        changefreq (str): The change frequency of the URL. Defaults to 'daily'.
        priority (float): The priority of the URL relative to other URLs on
        the site.

    """

    changefreq = "daily"
    priority = 0.6

    def items(self):
        """
        Method to return sitemap items.

        Returns:
            QuerySet: A queryset containing all Department objects.

        """
        return Department.objects.all()


class BlogSitemap(sitemaps.Sitemap):
    """
    Sitemap class for Blog model.

    This class generates sitemap entries for Blog objects.

    Attributes:
        changefreq (str): The change frequency of the URL. Defaults to 'daily'.
        priority (float): The priority of the URL relative to other URLs on
        the site.

    """

    changefreq = "daily"
    priority = 0.6

    def items(self):
        """
        Method to return sitemap items.

        Returns:
            QuerySet: A queryset containing all Blog objects.

        """
        return Blog.objects.all()

    def lastmod(self, obj):
        """
        Method to return the last modification time of a blog object.

        Args:
            obj: The Blog object.

        Returns:
            datetime: The last modification time of the blog object.

        """
        return obj.created
