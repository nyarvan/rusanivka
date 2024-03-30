from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import FormAdministration, FormDoctor, FormDepartment, FormBlog, BlogImageFormSet
from user_app.models import Contact, Blog, BlogImage, Administration, Doctor, Department
from .mixins import ManagerUserMixin


def is_manager(user):
    return user.groups.filter(name='manager').exists()


class ContactListView(ManagerUserMixin, ListView):
    template_name = 'contact-list.html'
    context_object_name = 'contacts'
    paginate_by = 5

    def get_queryset(self):
        return Contact.objects.filter(is_processing=False).order_by('-date')


@login_required(login_url='/login/')
@user_passes_test(is_manager)
def update_contact(request, pk):
    Contact.objects.filter(pk=pk).update(is_processing=True)
    return redirect('contact_list_view')


class CreateAdministrationView(ManagerUserMixin, CreateView):
    template_name = 'form_admin.html'
    form_class = FormAdministration
    success_url = '/administration/'


class CreateDoctorView(ManagerUserMixin, CreateView):
    template_name = 'form_doctor.html'
    form_class = FormDoctor

    def get_success_url(self):
        context = self.get_context_data()
        id = context['department'].id
        return f'/ambulant{id}/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = get_object_or_404(Department, id=self.kwargs.get('id'))
        return context


class CreateDepartmentView(ManagerUserMixin, CreateView):
    template_name = 'form_department.html'
    form_class = FormDepartment
    success_url = '/'


class BlogInline():
    form_class = FormBlog
    model = Blog
    template_name = "form_blog.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        
        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('user_app:blogs_view', slug=self.object.category.slug)

    def formset_image_valid(self, formset):
        images = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.blog = self.object
            image.save()


class CreateBlogView(ManagerUserMixin, BlogInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(CreateBlogView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'images': BlogImageFormSet(prefix='blog_images'),
            }
        else:
            return {
                'images': BlogImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='blog_images'),
            }
        

class UpdateBlogView(ManagerUserMixin, BlogInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(UpdateBlogView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['blog'] = self.object
        return ctx

    def get_named_formsets(self):
        return {
            'images': BlogImageFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='blog_images'),
        }


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_blog_image(request, pk):
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
    template_name = 'form_admin.html'
    form_class = FormAdministration
    success_url = '/administration/'

    def get_queryset(self):
        return Administration.objects.filter(id=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin'] = self.get_queryset().first()
        return context


class UpdateDoctorView(ManagerUserMixin, UpdateView):
    template_name = 'form_doctor.html'
    form_class = FormDoctor
    
    def get_queryset(self):
        return Doctor.objects.select_related('department').filter(id=self.kwargs.get('pk'))

    def get_success_url(self):
        context = self.get_context_data()
        id = context['department'].id
        return f'/ambulant{id}/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_queryset().first()
        context['doctor'] = doctor
        context['department'] = doctor.department
        return context


class UpdateDepartmentView(ManagerUserMixin, UpdateView):
    template_name = 'form_department.html'
    form_class = FormDepartment
    success_url = '/'

    def get_queryset(self):
        return Department.objects.filter(id=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = self.get_queryset().first()
        return context


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_administration(request, pk):
    Administration.objects.get(pk=pk).delete()
    return redirect('user_app:admin_view')


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_doctor(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    doctor.delete()
    return redirect('user_app:ambulant_view', id=doctor.department.id)


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_depart(request, pk):
    Department.objects.get(pk=pk).delete()
    return redirect('user_app:home_view')


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def delete_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    slug = blog.slug
    blog.delete()
    return redirect('user_app:blogs_view', slug=slug)
