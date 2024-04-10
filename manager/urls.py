from django.urls import path
from .views import ContactListView, update_contact, CreateAdministrationView, \
                    UpdateAdministrationView, delete_administration, \
                    CreateDoctorView, UpdateDoctorView, delete_doctor, \
                    CreateDepartmentView, UpdateDepartmentView, delete_depart, \
                    CreateBlogView, UpdateBlogView, delete_blog, \
                    delete_blog_image

urlpatterns = [
    path('contact-list/', ContactListView.as_view(), name='contact_list_view'),
    path(
        'contact-list/update/<int:pk>', update_contact, name='update_contact'),

    path(
        'administration/add/',
        CreateAdministrationView.as_view(),
        name='add_admin'),
    path(
        'administration/update/<int:pk>',
        UpdateAdministrationView.as_view(),
        name='update_admin'),
    path(
        'administration/delete/<int:pk>',
        delete_administration,
        name='delete_admin'),

    path(
        'ambulant<int:id>/doctors/add/',
        CreateDoctorView.as_view(),
        name='add_doctor'),
    path(
        'ambulant/doctors/update/<int:pk>',
        UpdateDoctorView.as_view(),
        name='update_doctor'),
    path(
        'ambulant/doctors/delete/<int:pk>',
        delete_doctor,
        name='delete_doctor'),

    path(
        'ambulant/add/',
        CreateDepartmentView.as_view(),
        name='add_depart'),
    path(
        'ambulant<int:pk>/update/',
        UpdateDepartmentView.as_view(),
        name='update_department'),
    path(
        'ambulant<int:pk>/delete/',
        delete_depart,
        name='delete_depart'),

    path('blogs/add/', CreateBlogView.as_view(), name='add_blog'),
    path(
        'blogs/update/<int:pk>/',
        UpdateBlogView.as_view(),
        name='update_blog'),
    path('blogs/delete/<int:pk>/', delete_blog, name='delete_blog'),
    path(
        'blogs/delete-image/<int:id>',
        delete_blog_image,
        name='delete_blog_image'),
]
