from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Department, Doctor, Administration, Blog, BlogImage, Document
from django.core.paginator import Paginator
from .forms import FormContact


def home_view(request):

    departments = Department.objects.all().order_by('number')
    doctors = Doctor.objects.filter(is_visible=True).order_by('name').distinct('name')[:4]
    blogs = Blog.objects.all().order_by('-create')[:3]

    return render(request, 'home.html', context={
        'departments': departments,
        'doctors': doctors,
        'blogs': blogs,
    })


def administration_view(request):

    admin = Administration.objects.all().order_by('position')
    blogs = Blog.objects.order_by('-create')[:3]

    return render(request, 'administration.html', context={
        'admins': admin,
        'blogs': blogs,
    })


def ambulant_view(request, id):

    manager = Doctor.objects.get(is_manager=True, department=id)
    doctors = Doctor.objects.filter(department=id, is_manager=False, is_visible=True).order_by('post')
    blogs = Blog.objects.order_by('-create')[:3]
    department = Department.objects.get(id=id)
    unvisible_doctors = Doctor.objects.filter(is_visible=False, department=id)

    return render(request, 'ambulant.html', context={
        'manager': manager,
        'doctors': doctors,
        'blogs': blogs,
        'department': department,
        'unvisible_doctor': unvisible_doctors
    })


def blogs_view(request):

    news = Blog.objects.all().order_by('-create')
    blogs = Blog.objects.order_by('-create')[:3]

    paginator = Paginator(news, 6)
    page = request.GET.get('page')

    news = paginator.get_page(page)

    return render(request, 'blogs.html', context={
        'news': news,
        'blogs': blogs,
    })


def blog_single_view(request, slug):

    item = get_object_or_404(Blog, slug=slug)
    images = BlogImage.objects.filter(blog=item.id)

    news = Blog.objects.order_by('-create')[:3]

    return render(request, 'blog_single.html', context={
        'item': item,
        'news': news,
        'blogs': news,
        'images': images,
    })


def contact_view(request):

    if request.method == 'POST':
        form = FormContact(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    form = FormContact()
    blogs = Blog.objects.order_by('-create')[:3]
    return render(request, 'contact.html', context={
        'form_contact': form,
        'blogs': blogs,
    })


def document_view(request):
    pass
