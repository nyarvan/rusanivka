from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class Department(models.Model):
    """
    Model representing a department.

    Attributes:
        name (str): The short name of the department.
        full_name (str): The full name of the department.
        number (int): The department number.
        manager (str): The manager of the department.
        image (str): The path to the image associated with the department.
        phone (str): The phone number of the department.
        address (str): The address of the department.
    """

    name = models.CharField(max_length=50, db_index=True, unique=True)
    full_name = models.CharField(max_length=75, unique=True)
    number = models.PositiveIntegerField(unique=True)
    manager = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to='images/departments', default='images/doctors/no-image.png')
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    class Meta:
        """
        Meta options for the Department model.

        Attributes:
            ordering (tuple): The default ordering for queryset results.
        """
        ordering = ('number', )

    def __str__(self):
        """
        Return a string representation of the department.

        Returns:
            str: The name of the department.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the absolute URL of the department's detail view.

        Returns:
            str: The absolute URL.
        """
        return reverse('user_app:ambulant_view', kwargs={'id': self.id, })


class Doctor(models.Model):
    """
    Model representing a doctor.

    Attributes:
        department (ForeignKey): The department to which the doctor belongs.
        name (str): The name of the doctor.
        image (str): The path to the image associated with the doctor.
        post (str): The post or position of the doctor.
        room (str): The room number of the doctor.
        schedule (str): The schedule or working hours of the doctor.
        is_manager (bool): Indicates whether the doctor is a manager
        of the department.
        is_visible (bool): Indicates whether the doctor is visible or active.
    """

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, db_index=True)
    image = models.ImageField(
        upload_to='images/doctors', default='images/doctors/no-image.png')
    post = models.CharField(max_length=100)
    room = models.CharField(max_length=50)
    schedule = models.TextField(blank=True)
    is_manager = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        """
        Meta options for the Doctor model.

        Attributes:
            ordering (tuple): The default ordering for queryset results.
        """
        ordering = ('department', '-is_manager', 'is_visible')

    def get_absolute_url(self):
        """
        Get the absolute URL of the doctor's detail view.

        Returns:
            str: The absolute URL.
        """
        return reverse(
            'user_app:ambulant_view', kwargs={'id': self.department.id, })

    def __str__(self):
        """
        Return a string representation of the doctor.

        Returns:
            str: The name of the doctor.
        """
        return self.name


class Administration(models.Model):
    """
    Model representing an administration member.

    Attributes:
        name (str): The name of the administration member.
        position (int): The position or rank of the administration member.
        image (str): The path to the image associated with
        the administration member.
        post (str): The post or position of the administration member.
        schedule (str): The schedule or working hours of
        the administration member.
        phone (str): The contact phone number of the administration member.
    """

    name = models.CharField(max_length=50, db_index=True)
    position = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to='images/administration',
        default='images/doctors/no-image.png')
    post = models.CharField(max_length=50)
    schedule = models.TextField(blank=True)
    phone = models.CharField(max_length=25)

    class Meta:
        """
        Meta options for the Administration model.

        Attributes:
            ordering (tuple): The default ordering for queryset results.
        """
        ordering = ('position', )

    def get_absolute_url(self):
        """
        Get the absolute URL of the administration member's detail view.

        Returns:
            str: The absolute URL.
        """
        return reverse('user_app:admin_view', kwargs={'id': self.id, })

    def __str__(self):
        """
        Return a string representation of the administration member.

        Returns:
            str: The name of the administration member.
        """
        return self.name


class CategoryBlog(models.Model):
    """
    Model representing a category for blog posts.

    Attributes:
        title (str): The title of the category.
        slug (str): The slugified version of the title used in URLs.
    """

    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    class Meta:
        """
        Meta options for the CategoryBlog model.

        Attributes:
            ordering (tuple): The default ordering for queryset results.
            index_together (tuple): The fields used together to
            enforce a unique constraint.
        """
        ordering = ('id', )
        index_together = (('id', 'slug'),)

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate the slug based on
        the title.
        """
        self.slug = slugify(self.title)
        super(CategoryBlog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Get the absolute URL of the category's detail view.

        Returns:
            str: The absolute URL.
        """
        return reverse('user_app:blogs_view', kwargs={'slug': self.slug, })

    def __str__(self):
        """
        Return a string representation of the category.

        Returns:
            str: The title of the category.
        """
        return self.title


class Blog(models.Model):
    """
    Model representing a blog post.

    Attributes:
        category (CategoryBlog): The category of the blog post.
        title (str): The title of the blog post.
        slug (str): The slugified version of the title used in URLs.
        image (str): The image associated with the blog post.
        text (str): The content of the blog post.
        create (datetime): The date and time when the blog post was created.
    """

    def get_default_category():
        """
        Helper function to get the default category for a blog post.

        Returns:
            CategoryBlog: The default category.
        """
        return CategoryBlog.objects.get(slug='novini')

    category = models.ForeignKey(
        CategoryBlog, on_delete=models.CASCADE, default=get_default_category)
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    image = models.ImageField(
        null=True, upload_to='images/blogs', default='images/doctors/no-image.png')
    file = models.FileField(null=True, upload_to='files/blogs')
    text = models.TextField(blank=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta options for the Blog model.

        Attributes:
            ordering (tuple): The default ordering for queryset results.
            index_together (tuple): The fields used together to enforce a
            unique constraint.
        """
        ordering = ('-create', 'category')
        index_together = (('id', 'slug'), )

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate the slug based on
        the title.
        """
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Get the absolute URL of the blog post's detail view.

        Returns:
            str: The absolute URL.
        """
        return reverse(
            'user_app:blog_single_view', kwargs={'slug': self.slug, })

    def __str__(self):
        """
        Return a string representation of the blog post.

        Returns:
            str: The title of the blog post.
        """
        return self.title


class BlogImage(models.Model):
    """
    Model representing an image associated with a blog post.

    Attributes:
        blog (Blog): The blog post to which the image belongs.
        image (str): The image file.
    """

    def get_length(self):
        """
        Get the total number of instances of BlogImage.

        Returns:
            int: The total number of instances.
        """
        return len(self.objects.all())

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/blogs', default='images/doctors/no-image.png')

    class Meta:
        """
        Meta options for the BlogImage model.

        Attributes:
            ordering (tuple): The default ordering for queryset results.
        """
        ordering = ('-blog',)

    def get_absolute_url(self):
        """
        Get the absolute URL of the blog image.

        Returns:
            str: The absolute URL.
        """
        return reverse('user_app:blog_single_view', kwargs={'id': self.id, })

    def __str__(self):
        """
        Return a string representation of the blog image.

        Returns:
            str: The string representation.
        """
        return f'{self.blog}'


class Document(models.Model):
    """
    Model representing a document.

    Attributes:
        name (str): The name of the document.
        file (File): The file field storing the document file.
    """

    name = models.CharField(max_length=50)
    file = models.FileField(upload_to="files/")

    class Meta:
        """
        Meta options for the Document model.

        Attributes:
            ordering (tuple): The default ordering for queryset results.
        """
        ordering = ('name', )

    def __str__(self):
        """
        Return a string representation of the document.

        Returns:
            str: The string representation.
        """
        return f'{self.name}'


class Contact(models.Model):
    """
    Model representing a contact form submission.

    Attributes:
        name (str): The name of the contact.
        email (Email): The email address of the contact.
        subject (str): The subject of the message.
        message (str): The message content.
        date (DateTime): The date and time of the submission.
        is_processing (bool): Indicates if the submission is being processed.
    """

    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_processing = models.BooleanField(default=False)

    class Meta:
        """
        Meta options for the Contact model.

        Attributes:
            ordering (tuple): The default ordering for queryset results.
        """
        ordering = ('-date', 'is_processing')

    def __str__(self):
        """
        Return a string representation of the contact form submission.

        Returns:
            str: The string representation.
        """
        return f'{self.name} {self.email} - {self.subject}'
