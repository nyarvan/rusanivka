from django.urls import path
from .views import home_view, administration_view, ambulant_view, blogs_view, blog_single_view, contact_view, \
    document_view


app_name = 'user_app'

urlpatterns = [
    path('', home_view, name='home_view'),
    path('administration/', administration_view, name='admin_view'),
    path('ambulant<int:id>/', ambulant_view, name='ambulant_view'),
    path('blog/news/', blogs_view, name='blogs_view'),
    path('blog/news/<slug:slug>/', blog_single_view, name='blog_single_view'),
    path('contact/', contact_view, name='contact_view'),
    path('documents/statut/', document_view, name='document_view'),
]