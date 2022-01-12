from django.contrib import admin
from .models import Department, Doctor, Administration, Blog, BlogImage, Contact, Document

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_name', 'number', 'manager', 'image', 'phone', 'address']
    list_filter = ['number',]
    list_editable = ['name', 'full_name', 'manager', 'image', 'phone', 'address']
    list_display_links = ['number',]

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['department', 'name', 'image', 'post', 'room', 'schedule', 'is_manager', 'is_visible']
    list_filter = ['department', 'post', 'is_manager', 'is_visible']
    list_editable = ['image', 'post', 'room', 'schedule', 'is_manager', 'is_visible']

@admin.register(Administration)
class AdministrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'image', 'post', 'schedule', 'phone']
    list_filter = ['position',]
    list_editable = ['position', 'image', 'post', 'schedule', 'phone']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'text', 'create']
    list_filter = ['create',]
    list_editable = ['image', 'text']
    list_display_links = ['title']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ['blog', 'image']
    list_filter = ['blog',]
    list_editable = ['image',]

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'file']
    list_filter = ['name',]
    list_editable = ['file',]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'date', 'is_processing']
    list_filter = ['date', 'is_processing']
    list_editable = ['is_processing',]