from django.urls import path
from django.views.generic.base import TemplateView
from .views import home_view, administration_view, ambulant_view, blogs_view, blog_single_view, contact_view, \
    document_view, SitemapXmlViews

app_name = 'user_app'

urlpatterns = [
    path('', home_view, name='home_view'),
    path('administration/', administration_view, name='admin_view'),
    path('ambulant<int:id>/', ambulant_view, name='ambulant_view'),
    path('blog/news/', blogs_view, name='blogs_view'),
    path('blog/news/<slug:slug>/', blog_single_view, name='blog_single_view'),
    path('contact/', contact_view, name='contact_view'),
    path('documents/statut/', document_view, name='document_view'),

    path('sitemap.xml', SitemapXmlViews.as_view()),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
