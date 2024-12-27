from django.urls import path
from .views import HomepageView, AdministrationView, DepartmentView, \
                    BlogsView, BlogDetailView, ContactView, DrugsView, \
                    MedicalServicesView, FreeMedicalServicesView

app_name = 'user_app'

urlpatterns = [
    path('', HomepageView.as_view(), name='home_view'),
    path('administration/', AdministrationView.as_view(), name='admin_view'),
    path('ambulant<int:id>/', DepartmentView.as_view(), name='ambulant_view'),
    path('information-for-clients/medicines/',
         DrugsView.as_view(), name='drugs_view'),
     path('information-for-clients/services/unpaid/', FreeMedicalServicesView.as_view(), name='free_medical_services'),
     path('information-for-clients/services/paid/', MedicalServicesView.as_view(), name='medical_services'),
    path('blog/<slug:slug>/', BlogsView.as_view(), name='blogs_view'),
    path('blog/<slug:slug_category>/<int:id>/<slug:slug>/',
         BlogDetailView.as_view(), name='blog_single_view'),
    path('contact/', ContactView.as_view(), name='contact_view'),
]
