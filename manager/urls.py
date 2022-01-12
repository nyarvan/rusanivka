from django.urls import path
from .views import contact_list_view, update_contact, add_administration, update_administration, delete_administration, \
    add_doctor, update_doctor, delete_doctor, add_department, update_department, delete_depart, add_blog, update_blog, \
    delete_blog, add_blog_image, update_blog_image, delete_blog_image

urlpatterns = [
    path('contact-list/', contact_list_view, name='contact_list_view'),
    path('contact-list/update/<int:pk>', update_contact, name='update_contact'),

    path('administration/add/', add_administration, name='add_admin'),
    path('administration/update/<int:pk>', update_administration, name='update_admin'),
    path('administration/delete/<int:pk>', delete_administration, name='delete_admin'),

    path('ambulant<int:id>/doctors/add/', add_doctor, name='add_doctor'),
    path('ambulant/doctors/update/<int:pk>', update_doctor, name='update_doctor'),
    path('ambulant/doctors/delete/<int:pk>', delete_doctor, name='delete_doctor'),

    path('ambulant/add/', add_department, name='add_depart'),
    path('ambulant<int:pk>/update/', update_department, name='update_department'),
    path('ambulant<int:pk>/delete/', delete_depart, name='delete_depart'),

    path('blogs/add/', add_blog, name='add_blog'),
    path('blogs/<slug:slug>/add-image/', add_blog_image, name='add_blog_image'),
    path('blogs/update/<int:pk>/', update_blog, name='update_blog'),
    path('blogs/<slug:slug>/update-image/<int:id>', update_blog_image, name='update_blog_image'),
    path('blogs/delete/<int:pk>/', delete_blog, name='delete_blog'),
    path('blogs/<slug:slug>/delete-image/<int:id>', delete_blog_image, name='delete_blog_image'),
]