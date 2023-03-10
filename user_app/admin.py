from django.contrib import admin
from .models import Department, Doctor, Administration, Blog, BlogImage, Contact, Document


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'image']
    list_filter = ['number', ]
    list_editable = ['name', 'manager', 'image']
    list_display_links = ['name', ]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'post', 'department', 'is_manager', 'is_visible']
    list_filter = ['department', 'post', 'is_manager', 'is_visible']
    list_editable = ['image', 'post', 'is_manager', 'is_visible']
    list_display_links = ['name', ]


@admin.register(Administration)
class AdministrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'post']
    list_filter = ['position', ]
    list_editable = ['image', 'post']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'create']
    list_filter = ['create', ]
    list_editable = ['image', ]
    list_display_links = ['title', ]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ['blog', 'image']
    list_filter = ['blog', ]
    list_editable = ['image', ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'file']
    list_filter = ['name', ]
    list_editable = ['file', ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'date', 'is_processing']
    list_filter = ['date', 'is_processing']
    list_editable = ['is_processing', ]
