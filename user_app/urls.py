from django.urls import path
from .views import HomepageView, AdministrationView, DepartmentView, BlogsView, BlogDetailView, ContactView, \
    document_view

app_name = 'user_app'

urlpatterns = [
    path('', HomepageView.as_view(), name='home_view'),
    path('administration/', AdministrationView.as_view(), name='admin_view'),
    path('ambulant<int:id>/', DepartmentView.as_view(), name='ambulant_view'),
    path('blog/news/', BlogsView.as_view(), name='blogs_view'),
    path('blog/news/<slug:slug>/', BlogDetailView.as_view(), name='blog_single_view'),
    path('contact/', ContactView.as_view(), name='contact_view'),
    path('documents/statut/', document_view, name='document_view'),
]
