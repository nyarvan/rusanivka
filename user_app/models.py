from django.db import models
from os import path
from uuid import uuid4
from django.urls import reverse
from pytils.translit import slugify


class Department(models.Model):
    
    name = models.CharField(max_length=50, db_index=True, unique=True)
    full_name = models.CharField(max_length=75, unique=True)
    number = models.PositiveIntegerField(unique=True)
    manager = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/departments', default='images/doctors/no-image.png')
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    class Meta:
        ordering = ('number', )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('user_app:ambulant_view', kwargs={'id': self.id})


class Doctor(models.Model):

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, db_index=True)
    image = models.ImageField(upload_to='images/doctors', default='images/doctors/no-image.png')
    post = models.CharField(max_length=100)
    room = models.CharField(max_length=50)
    schedule = models.TextField(blank=True)
    is_manager = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ('department', '-is_manager', 'is_visible')

    def get_absolute_url(self):
        return reverse('user_app:ambulant_view', kwargs={'id': self.department.id})

    def __str__(self):
        return f'{self.name}'


class Administration(models.Model):

    name = models.CharField(max_length=50, db_index=True)
    position = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/administration', default='images/doctors/no-image.png')
    post = models.CharField(max_length=50)
    schedule = models.TextField(blank=True)
    phone = models.CharField(max_length=25)

    class Meta:
        ordering = ('position',)

    def get_absolute_url(self):
        return reverse('user_app:admin_view', kwargs={'id': self.id})

    def __str__(self):
        return f'{self.name}'


class Blog(models.Model):

    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    image = models.ImageField(upload_to='images/blogs', default='images/doctors/no-image.png')
    text = models.TextField(blank=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-create',)
        index_together = (('id', 'slug'),)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_app:blog_single_view', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'


class BlogImage(models.Model):

    def get_length(self):
        length = len(self.objects.all())
        return length

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/blogs', default='images/doctors/no-image.png')

    class Meta:
        ordering = ('-blog',)

    def get_absolute_url(self):
        return reverse('user_app:blog_single_view', kwargs={'id': self.id})

    def __str__(self):
        return f'{self.blog}'


class Document(models.Model):

    name = models.CharField(max_length=50)
    file = models.FileField(upload_to="files/")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Contact(models.Model):

    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_processing = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date', 'is_processing')

    def __str__(self):
        return f'{self.name} {self.email} - {self.subject}'
