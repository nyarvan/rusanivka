from django.contrib import admin
from .models import Department, Doctor, Administration, CategoryBlog, Blog, \
                        BlogImage, Contact, Document


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Administration class for Department model.

    Attributes:
        list_display (list): The fields to be displayed in the list view of
        the admin interface.
        list_filter (list): The fields to be used as filters in the list view.
        list_editable (list): The fields that can be edited directly in
        the list view.
        list_display_links (list): The fields to be linked to the detail view
        in the list view.
    """
    list_display = ['name', 'manager', 'image']
    list_filter = ['number', ]
    list_editable = ['manager', 'image']
    list_display_links = ['name', ]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Administration class for Doctor model.

    Attributes:
        list_display (list): The fields to be displayed in the list view of
        the admin interface.
        list_filter (list): The fields to be used as filters in the list view.
        list_editable (list): The fields that can be edited directly in
        the list view.
        list_display_links (list): The fields to be linked to the detail view
        in the list view.
        search_fields (list): The fields to be searched in the list view.
    """
    list_display = [
        'name', 'image', 'post',
        'department', 'is_manager', 'is_visible']
    list_filter = ['department', 'post', 'is_manager', 'is_visible']
    list_editable = ['image', 'post', 'is_manager', 'is_visible']
    list_display_links = ['name', ]
    search_fields = ['name', ]


@admin.register(Administration)
class AdministrationAdmin(admin.ModelAdmin):
    """
    Administration class for Administration model.

    Attributes:
        list_display (list): The fields to be displayed in the list view of
        the admin interface.
        list_filter (list): The fields to be used as filters in the list view.
        list_editable (list): The fields that can be edited directly in
        the list view.
        list_display_links (list): The fields to be linked to the detail view
        in the list view.
    """
    list_display = ['name', 'image', 'post']
    list_filter = ['position', ]
    list_editable = ['image', 'post']
    list_display_links = ['name', ]


class BlogImageAdmin(admin.TabularInline):
    """
    BlogImage class for admin inline editing.

    This class allows inline editing of BlogImage objects within
    the admin interface.

    Attributes:
        model (Model): The model associated with this inline.
        raw_id_fields (list): The fields for which raw IDs are used instead of
        the more human-friendly select boxes.
    """
    model = BlogImage
    raw_id_fields = ['blog', ]


@admin.register(CategoryBlog)
class CategoryBlogAdmin(admin.ModelAdmin):
    """
    CategoryBlog class for admin interface.

    This class defines the appearance and behavior of the CategoryBlog model
    in the Django admin interface.

    Attributes:
        list_display (list): The list of fields to display
        in the admin list view.
        list_display_links (list): The list of fields to use as links
        in the admin list view.
        prepopulated_fields (dict): A dictionary specifying which fields
        should be prepopulated based on other fields.
    """
    list_display = ['title', 'slug']
    list_display_links = ['title', ]
    prepopulated_fields = {'slug': ('title', ), }


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Blog class for admin interface.

    This class defines the appearance and behavior of the Blog model
    in the Django admin interface.

    Attributes:
        list_display (list): The list of fields to display
        in the admin list view.
        list_editable (list): The list of fields that can be edited directly
        in the admin list view.
        list_filter (list): The list of fields to filter by
        in the admin list view.
        list_display_links (list): The list of fields to use as links
        in the admin list view.
        prepopulated_fields (dict): A dictionary specifying which fields
        should be prepopulated based on other fields.
        search_fields (list): The list of fields to search by
        in the admin interface.
        inlines (list): The list of inline classes to include
        in the admin interface.
    """
    list_display = ['category', 'title', 'slug', 'image', 'file', 'create']
    list_editable = ['image', 'file']
    list_filter = ['category', ]
    list_display_links = ['title', ]
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ['title', 'text']
    inlines = [BlogImageAdmin, ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Document class for admin interface.

    This class defines the appearance and behavior of the Document model
    in the Django admin interface.

    Attributes:
        list_display (list): The list of fields to display
        in the admin list view.
        list_filter (list): The list of fields to filter by
        in the admin list view.
        list_editable (list): The list of fields that can be edited directly
        in the admin list view.
    """
    list_display = ['name', 'file']
    list_filter = ['name', ]
    list_editable = ['file', ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Contact class for admin interface.

    This class defines the appearance and behavior of the Contact model
    in the Django admin interface.

    Attributes:
        list_display (list): The list of fields to display
        in the admin list view.
        list_filter (list): The list of fields to filter by
        in the admin list view.
        list_editable (list): The list of fields that can be edited directly
        in the admin list view.
        search_fields (list): The list of fields to search by
        in the admin interface.
    """
    list_display = ['name', 'email', 'subject', 'date', 'is_processing']
    list_filter = ['date', 'is_processing']
    list_editable = ['is_processing', ]
    search_fields = ['name', 'email']
