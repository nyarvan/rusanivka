from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from user_app.models import Contact, Blog, BlogImage, \
                                Administration, Doctor, Department
from .forms import FormAdministration, FormDoctor, FormDepartment, \
                    FormBlog, BlogImageFormSet
from .mixins import ManagerUserMixin


def is_manager(user):
    """
    Check if the user belongs to the 'manager' group.

    Args:
        user: The user object to check.

    Returns:
        bool: True if the user belongs to the 'manager' group, False otherwise.
    """
    return user.groups.filter(name='manager').exists()


class ContactListView(ManagerUserMixin, ListView):
    """
    View for displaying a list of contacts.

    This view is accessible only to users with 'manager' group permissions.
    It displays a list of contacts that are not marked as processing.

    Attributes:
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the context variable containing
        the list of contacts.
        paginate_by (int): The number of contacts to display per page.

    """

    template_name = 'contact-list.html'
    context_object_name = 'contacts'
    paginate_by = 5

    def get_queryset(self):
        """
        Method to return the queryset of contacts.

        Returns:
            QuerySet: A queryset containing contacts that are not marked as
            processing, ordered by date.

        """
        return Contact.objects.filter(is_processing=False).order_by('-date')


@login_required(login_url='/login/')
@user_passes_test(is_manager)
def update_contact(request, pk):
    """
    Update the processing status of a contact.

    If the user is a manager and logged in, this view updates the processing
    status of the contact with the given primary key to True.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the contact to be updated.

    Returns:
        HttpResponseRedirect: Redirects to the contact list view
        after updating.
    """
    Contact.objects.filter(pk=pk).update(is_processing=True)
    return redirect('contact_list_view')


class CreateAdministrationView(ManagerUserMixin, CreateView):
    """
    View for creating a new administration entry.

    This view allows managers to create a new administration entry using
    the provided form.

    Attributes:
        template_name (str): The name of the template to render.
        form_class (class): The form class to use for creating the
        administration entry.
        success_url (str): The URL to redirect to after successfully creating
        the entry.

    """
    template_name = 'form_admin.html'
    form_class = FormAdministration
    success_url = '/administration/'


class CreateDoctorView(ManagerUserMixin, CreateView):
    """
    View for creating a new doctor entry.

    This view allows managers to create a new doctor entry using
    the provided form.

    Attributes:
        template_name (str): The name of the template to render.
        form_class (class): The form class to use for creating
        the doctor entry.

    Methods:
        get_success_url: Returns the URL to redirect to after successfully
        creating the entry.
        get_context_data: Returns the context data to be used in the template.

    """
    template_name = 'form_doctor.html'
    form_class = FormDoctor

    def get_success_url(self):
        """
        Returns the URL to redirect to after successfully creating the entry.

        Returns:
            str: The success URL.
        """
        context = self.get_context_data()
        department_id = context['department'].id
        return f'/ambulant{department_id}/'

    def get_context_data(self, **kwargs):
        """
        Returns the context data to be used in the template.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context['department'] = get_object_or_404(
                                    Department, id=self.kwargs.get('id'))
        return context


class CreateDepartmentView(ManagerUserMixin, CreateView):
    """
    View for creating a new department entry.

    This view allows managers to create a new department entry using
    the provided form.

    Attributes:
        template_name (str): The name of the template to render.
        form_class (class): The form class to use for creating
        the department entry.
        success_url (str): The URL to redirect to after successfully creating
        the entry.

    """
    template_name = 'form_department.html'
    form_class = FormDepartment
    success_url = '/'


class BlogInline():
    """
    Inline formset for managing blog images.

    This class provides functionality for managing blog images within
    the blog creation form.

    Attributes:
        form_class (class): The form class to use for managing blog images.
        model (class): The model class representing blog images.
        template_name (str): The name of the template to render.

    """
    form_class = FormBlog
    model = Blog
    template_name = "form_blog.html"

    def form_valid(self, form):
        """
        Method to handle form validation and saving.

        This method validates the form and saves the data. It also handles
        the saving of related formsets
        for managing blog images.

        Returns:
            HttpResponseRedirect: A redirect response to the single blog view.

        """
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect(
            'user_app:blog_single_view',
            slug_category=self.object.category.slug,
            id=self.object.id,
            slug=self.object.slug)

    def formset_image_valid(self, formset):
        """
        Method to handle valid image formset data.

        This method saves the image objects associated with the blog.

        Args:
            formset (FormSet): The formset containing the image data.

        """
        images = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.blog = self.object
            image.save()


class CreateBlogView(ManagerUserMixin, BlogInline, CreateView):
    """
    View for creating a new blog entry.

    This view provides functionality for creating a new blog entry, including
    handling form validation and
    managing related formsets for blog images.

    """

    def get_context_data(self, **kwargs):
        """
        Method to get context data for the view.

        This method retrieves and adds additional context data for rendering
        the template.

        Returns:
            dict: The context data for the view.

        """
        ctx = super(CreateBlogView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        """
        Method to get named formsets.

        This method retrieves and initializes formsets for managing related
        objects, such as blog images.

        Returns:
            dict: A dictionary containing the initialized formsets.

        """
        if self.request.method == "GET":
            return {
                'images': BlogImageFormSet(prefix='blog_images'),
            }
        else:
            return {
                'images': BlogImageFormSet(
                    self.request.POST or None,
                    self.request.FILES or None,
                    prefix='blog_images'),
            }


class UpdateBlogView(ManagerUserMixin, BlogInline, UpdateView):
    """
    View for updating a blog entry.

    This view provides functionality for updating an existing blog entry,
    including handling form validation and
    managing related formsets for blog images.

    """

    def get_context_data(self, **kwargs):
        """
        Method to get context data for the view.

        This method retrieves and adds additional context data for rendering
        the template.

        Returns:
            dict: The context data for the view.

        """
        ctx = super(UpdateBlogView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['blog'] = self.object
        return ctx

    def get_named_formsets(self):
        """
        Method to get named formsets.

        This method retrieves and initializes formsets for managing related
        objects, such as blog images.

        Returns:
            dict: A dictionary containing the initialized formsets.

        """
        return {
            'images': BlogImageFormSet(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix='blog_images'),
        }


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_blog_image(request, pk):
    """
    View function for deleting a blog image.

    This view function allows authorized users with manager privileges to
    delete a blog image.
    If the image with the given primary key (pk) is found, it is deleted from
    the database.
    If the image is not found, a success message is displayed, and the user is
    redirected to the update view
    of the corresponding blog entry.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the blog image to be deleted.

    Returns:
        HttpResponseRedirect: Redirects the user to the update view of
        the corresponding blog entry after
        deleting the image.

    """
    try:
        image = BlogImage.objects.get(id=pk)
    except BlogImage.DoesNotExist:
        messages.success(
            request, 'Зображення не знайдено'
            )
        return redirect('update_blog', pk=image.blog.id)

    image.delete()
    messages.success(
            request, 'Зображення видалено вдачно'
            )
    return redirect('update_blog', pk=image.blog.id)


class UpdateAdministrationView(ManagerUserMixin, UpdateView):
    """
    View class for updating administration details.

    This view class allows authorized users with manager privileges to update
    administration details.
    It extends the UpdateView class provided by Django and specifies
    the template, form class, success URL,
    and queryset to be used for updating administration objects.

    Attributes:
        template_name (str): The name of the template used for rendering
        the update administration form.
        form_class (FormAdministration): The form class used for updating
        administration details.
        success_url (str): The URL to redirect to after successfully updating
        administration details.

    Methods:
        get_queryset(self): Returns the queryset of administration objects
        filtered by the primary key (pk).
        get_context_data(self, **kwargs): Adds additional context data to be
        passed to the template,
            including the administration object being updated.

    """
    template_name = 'form_admin.html'
    form_class = FormAdministration
    success_url = '/administration/'

    def get_queryset(self):
        """
        Method to get the queryset of administration objects.

        Returns:
            QuerySet: The filtered queryset of administration objects,
            filtered by the primary key (pk).

        """
        return Administration.objects.filter(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        """
        Method to get the context data for rendering the template.

        Adds the administration object being updated to the context data.

        Returns:
            dict: The context data dictionary.

        """
        context = super().get_context_data(**kwargs)
        context['admin'] = self.get_queryset().first()
        return context


class UpdateDoctorView(ManagerUserMixin, UpdateView):
    """
    View class for updating doctor details.

    This view class allows authorized users with manager privileges to update
    doctor details.
    It extends the UpdateView class provided by Django and specifies
    the template, form class,
    queryset, and success URL to be used for updating doctor objects.

    Attributes:
        template_name (str): The name of the template used for rendering
        the update doctor form.
        form_class (FormDoctor): The form class used for updating doctor
        details.
        queryset (QuerySet): The queryset of doctor objects filtered by
        the primary key (pk).
        success_url (str): The URL to redirect to after successfully updating
        doctor details.

    Methods:
        get_queryset(self): Returns the queryset of doctor objects filtered by
        the primary key (pk),
            and selects related department objects to minimize database
            queries.
        get_success_url(self): Returns the success URL after successfully
        updating doctor details,
            based on the associated department of the doctor.
        get_context_data(self, **kwargs): Adds additional context data to be
        passed to the template,
            including the doctor object being updated and its associated
            department.

    """
    template_name = 'form_doctor.html'
    form_class = FormDoctor

    def get_queryset(self):
        """
        Method to get the queryset of doctor objects.

        Returns:
            QuerySet: The filtered queryset of doctor objects, filtered by
            the primary key (pk),
                with related department objects selected to minimize database
                queries.

        """
        return Doctor.objects.select_related('department').filter(
            id=self.kwargs.get('pk'))

    def get_success_url(self):
        """
        Method to get the success URL after updating doctor details.

        Returns:
            str: The success URL, based on the associated department of
            the doctor.

        """
        context = self.get_context_data()
        department_id = context['department'].id
        return f'/ambulant{department_id}/'

    def get_context_data(self, **kwargs):
        """
        Method to get the context data for rendering the template.

        Adds the doctor object being updated and its associated department to
        the context data.

        Returns:
            dict: The context data dictionary.

        """
        context = super().get_context_data(**kwargs)
        doctor = self.get_queryset().first()
        context['doctor'] = doctor
        context['department'] = doctor.department
        return context


class UpdateDepartmentView(ManagerUserMixin, UpdateView):
    """
    View class for updating department details.

    This view class allows authorized users with manager privileges to update
    department details.
    It extends the UpdateView class provided by Django and specifies
    the template, form class,
    queryset, and success URL to be used for updating department objects.

    Attributes:
        template_name (str): The name of the template used for rendering
        the update department form.
        form_class (FormDepartment): The form class used for updating
        department details.
        success_url (str): The URL to redirect to after successfully updating
        department details.

    Methods:
        get_queryset(self): Returns the queryset of department objects
        filtered by the primary key (pk).
        get_context_data(self, **kwargs): Adds additional context data to be
        passed to the template,
            including the department object being updated.

    """
    template_name = 'form_department.html'
    form_class = FormDepartment
    success_url = '/'

    def get_queryset(self):
        """
        Method to get the queryset of department objects.

        Returns:
            QuerySet: The filtered queryset of department objects, filtered by
            the primary key (pk).

        """
        return Department.objects.filter(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        """
        Method to get the context data for rendering the template.

        Adds the department object being updated to the context data.

        Returns:
            dict: The context data dictionary.

        """
        context = super().get_context_data(**kwargs)
        context['department'] = self.get_queryset().first()
        return context


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_administration(request, pk):
    """
    View function for deleting an administration instance.

    This view function deletes the administration instance with the given
    primary key (pk) from the database.
    It requires the user to be logged in and have manager privileges.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the administration instance to delete.

    Returns:
        HttpResponseRedirect: Redirects to the administration list view after
        successful deletion.

    """
    Administration.objects.get(pk=pk).delete()
    return redirect('user_app:admin_view')


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_doctor(request, pk):
    """
    View function for deleting a doctor instance.

    This view function deletes the doctor instance with the given primary key
    (pk) from the database.
    It requires the user to be logged in and have manager privileges.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the doctor instance to delete.

    Returns:
        HttpResponseRedirect: Redirects to the department view associated with
        the deleted doctor after successful deletion.

    """
    doctor = Doctor.objects.get(pk=pk)
    doctor.delete()
    return redirect('user_app:ambulant_view', id=doctor.department.id)


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_depart(request, pk):
    """
    View function for deleting a department instance.

    This view function deletes the department instance with the given primary
    key (pk) from the database.
    It requires the user to be logged in and have manager privileges.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the department instance to delete.

    Returns:
        HttpResponseRedirect: Redirects to the home view after successful
        deletion.

    """
    Department.objects.get(pk=pk).delete()
    return redirect('user_app:home_view')


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_blog(request, pk):
    """
    View function for deleting a blog instance.

    This view function deletes the blog instance with the given primary key
    (pk) from the database.
    It requires the user to be logged in and have manager privileges.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the blog instance to delete.

    Returns:
        HttpResponseRedirect: Redirects to the blogs view associated with
        the deleted blog's category after successful deletion.

    """
    blog = Blog.objects.get(pk=pk)
    slug = blog.category.slug
    blog.delete()
    return redirect('user_app:blogs_view', slug=slug)
