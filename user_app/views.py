from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from .models import Department, Doctor, Administration, Blog, BlogImage
from .forms import FormContact


class HomepageView(ListView):
    template_name = 'home.html'
    context_object_name = 'departments'

    def get_queryset(self):
        return Department.objects.all().order_by('number')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['doctors'] = Doctor.objects.filter(is_visible=True, is_manager=False).order_by('?')[:4]
        return context


class AdministrationView(ListView):
    template_name = 'administration.html'
    context_object_name = 'admins'

    def get_queryset(self):
        return Administration.objects.all().order_by('position')


class DepartmentView(ListView):
    template_name = 'ambulant.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        id = self.kwargs.get('id')
        return Doctor.objects.filter(department=id, is_manager=False, is_visible=True).order_by('post')
    
    def get_context_data(self, **kwargs):
        id = self.kwargs.get('id')
        context = super().get_context_data(**kwargs)
        context['manager'] = Doctor.objects.get(is_manager=True, department=id)
        context['department'] = get_object_or_404(Department, id=id)
        context['unvisible_doctor'] = Doctor.objects.filter(is_visible=False, department=id)
        return context
    

class BlogsView(ListView):
    template_name = 'blogs.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_queryset(self):
        return Blog.objects.all().order_by('-create')
    

class BlogDetailView(DetailView):
    template_name = 'blog_single.html'
    context_object_name = 'blog'
    model = Blog

    def get_object(self, queryset):
        return get_object_or_404(Blog, id=self.kwargs.get('id'), slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = BlogImage.objects.filter(blog=self.get_object())
        return context


class ContactView(FormView):
    form_class = FormContact
    template_name = 'contact.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(ContactView, self).form_valid(form)


def document_view(request):
    pass
