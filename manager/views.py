from django.shortcuts import render, redirect
from user_app.models import Contact, Blog, BlogImage
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FormAdministration, FormDoctor, FormDepartment, FormBlog, FormBlogImage
from user_app.models import Administration, Doctor, Department

def is_manager(user):
    return user.groups.filter(name='manager').exists()

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def contact_list_view(request):
    contacts = Contact.objects.filter(is_processing=False).order_by('-date')
    blogs = Blog.objects.order_by('-create')[:3]

    paginator = Paginator(contacts, 5)
    page = request.GET.get('page')

    contacts = paginator.get_page(page)

    return render(request, 'contact-list.html', context={
        'blogs': blogs,
        'contacts': contacts,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def update_contact(request, pk):
    Contact.objects.filter(pk=pk).update(is_processing=True)
    return redirect('contact_list_view')

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def add_administration(request):
    form_administration = FormAdministration(request.POST, request.FILES or None)

    if form_administration.is_valid():
        form_administration.save()
        return redirect('user_app:admin_view')

    return render(request, 'add_admin.html', context={
        'form': form_administration,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def add_doctor(request, id):
    form_doctor = FormDoctor(request.POST, request.FILES or None)
    department = Department.objects.get(id=id)
    if form_doctor.is_valid():
        form_doctor.save()
        return redirect('user_app:ambulant_view', id=id)

    return render(request, 'add_doctor.html', context={
        'form': form_doctor,
        'department': department,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def add_department(request):
    form_depart = FormDepartment(request.POST, request.FILES or None)

    if form_depart.is_valid():
        form_depart.save()
        return redirect('user_app:home_view')

    return render(request, 'add_depart.html', context={
        'form': form_depart,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def add_blog(request):
    form_blog = FormBlog(request.POST, request.FILES or None)

    if form_blog.is_valid():
        form_blog.save()
        return redirect('user_app:blogs_view')

    return render(request, 'add_blog.html', context={
        'form': form_blog,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def add_blog_image(request, slug):
    blog = Blog.objects.get(slug=slug)

    form_blog_image = FormBlogImage(request.POST, request.FILES or None)

    if form_blog_image.is_valid():
        form_blog_image.save()
        return redirect('user_app:blog_single_view', slug=blog.slug)

    return render(request, 'add_blog_image.html', context={
        'blog': blog,
        'form': form_blog_image,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def update_administration(request, pk):
    admin = Administration.objects.get(pk=pk)
    if request.method == 'POST':
        form_admin = FormAdministration(request.POST, request.FILES, instance=admin)
        if form_admin.is_valid():
            form_admin.save()
            return redirect('user_app:admin_view')

    form_admin = FormAdministration(instance=admin)
    return render(request, 'update_admin.html', context={
        'form': form_admin,
        'admin': admin,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def update_doctor(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    if request.method == "POST":
        form_doctor = FormDoctor(request.POST, request.FILES, instance=doctor)
        if form_doctor.is_valid():
            form_doctor.save()
            return redirect('user_app:ambulant_view', id=doctor.department.id)

    form_doctor = FormDoctor(instance=doctor)
    return render(request, 'update_doctor.html', context={
        'doctor': doctor,
        'form': form_doctor,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def update_department(request, pk):
    department = Department.objects.get(pk=pk)
    if request.method == 'POST':
        form_depart = FormDepartment(request.POST, request.FILES, instance=department)
        if form_depart.is_valid():
            form_depart.save()
            return redirect('user_app:home_view')

    form_depart = FormDepartment(instance=department)
    return render(request, 'update_department.html', context={
        'department': department,
        'form': form_depart,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def update_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    if request.method == 'POST':
        form_blog = FormBlog(request.POST, request.FILES, instance=blog)
        if form_blog.is_valid():
            form_blog.save()
            return redirect('user_app:blog_single_view', slug=blog.slug)

    form_blog = FormBlog(instance=blog)
    return render(request, 'update_blog.html', context={
        'blog': blog,
        'form': form_blog,
    })

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def update_blog_image(request, slug, id):
    blog = Blog.objects.get(slug=slug)
    blog_image = BlogImage.objects.get(blog=blog, id=id)
    if request.method == 'POST':
        form_blog_image = FormBlogImage(request.POST, request.FILES, instance=blog_image)
        if form_blog_image.is_valid():
            form_blog_image.save()
            return redirect('user_app:blog_single_view', slug=blog_image.blog.slug)

    form_blog_image = FormBlogImage(instance=blog_image)
    return render(request, 'update_blog_image.html', context={
        'blog_image': blog_image,
        'form': form_blog_image,
    })

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
    Blog.objects.get(pk=pk).delete()
    return redirect('user_app:blogs_view')

def delete_blog_image(request, id, slug):
    BlogImage.objects.get(id=id).delete()
    blog = Blog.objects.get(slug=slug)

    return redirect('user_app:blog_single_view', slug=blog.slug)
