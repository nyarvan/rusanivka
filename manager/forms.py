from django import forms
from django.forms import inlineformset_factory
from user_app.models import Administration, Doctor, Department, Blog, BlogImage


class FormAdministration(forms.ModelForm):
    """
    Form class for Administration model.

    This form is used to create or update Administration instances.

    Attributes:
        name (str): The name of the administrator.
        position (decimal): The position of the administrator.
        image (file): The image of the administrator.
        post (str): The post of the administrator.
        schedule (str): The work schedule of the administrator.
        phone (str): The phone number of the administrator.

    """
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter full name",
    }))

    position = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter position",
    }))

    image = forms.FileField()

    post = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter post",
    }))

    schedule = forms.CharField(widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows': "5",
        'placeholder': "Enter work schedule",
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter phone number",
    }))

    class Meta:
        """
        Metadata options for the FormAdministration form.

        Attributes:
            model (class): Specifies the model class that the form
            interacts with.
            fields (tuple): Specifies the fields from the model to include in
            the form.

        """
        model = Administration
        fields = ('name', 'position', 'image', 'post', 'schedule', 'phone')


class FormDoctor(forms.ModelForm):
    """
    Form for creating and updating Doctor instances.

    This form provides fields for the user to input data necessary to create
    or update a Doctor instance.

    Attributes:
        name (CharField): Field for entering the name of the doctor.
        image (FileField): Field for uploading an image of the doctor.
        post (CharField): Field for entering the post/title of the doctor.
        room (CharField): Field for entering the room/office number of
        the doctor.
        schedule (CharField): Field for entering the schedule of the doctor.

    Meta:
        model (class): Specifies the model class that the form interacts with.
        fields (tuple): Specifies the fields from the model to include in
        the form.

    """
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter name",
    }))

    image = forms.FileField(required=False)

    post = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter post/title",
    }))

    room = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter room/office number",
    }))

    schedule = forms.CharField(widget=forms.Textarea(attrs={
        'class': "form-control", 'rows': "5", 'placeholder': "Enter schedule",
    }))

    class Meta:
        """
        Metadata options for the FormDoctor form.

        Attributes:
            model (class): Specifies the model class that the form
            interacts with.
            fields (tuple): Specifies the fields from the model to include in
            the form.

        """
        model = Doctor
        fields = (
            'department', 'name', 'image', 'post',
            'room', 'schedule', 'is_manager', 'is_visible'
        )


class FormDepartment(forms.ModelForm):
    """
    Form for creating and updating Department instances.

    This form provides fields for the user to input data necessary to create
    or update a Department instance.

    Attributes:
        name (CharField): Field for entering the name of the department.
        full_name (CharField): Field for entering the full name of
        the department.
        number (DecimalField): Field for entering the number of the department.
        manager (CharField): Field for entering the name of the manager of
        the department.
        image (FileField): Field for uploading an image of the department.
        phone (CharField): Field for entering the phone number of
        the department.
        address (CharField): Field for entering the address of the department.

    Meta:
        model (class): Specifies the model class that the form interacts with.
        fields (tuple): Specifies the fields from the model to include
        in the form.

    """
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter department name",
    }))

    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter full department name",
    }))

    number = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter department number",
    }))

    manager = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter manager's name",
    }))

    image = forms.FileField()

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Enter department phone number",
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter department address",
    }))

    class Meta:
        """
        Metadata options for the FormDepartment form.

        Attributes:
            model (class): Specifies the model class that the form interacts
            with.
            fields (tuple): Specifies the fields from the model to include in
            the form.

        """
        model = Department
        fields = (
            'name', 'full_name', 'number',
            'manager', 'image', 'phone',
            'address'
        )


class FormBlog(forms.ModelForm):
    """
    Form for creating and updating Blog instances.

    This form provides fields for the user to input data necessary to create
    or update a Blog instance.

    Attributes:
        title (CharField): Field for entering the title of the blog post.
        image (FileField): Field for uploading an image for the blog post.
        text (CharField): Field for entering the text content of the blog post.

    Meta:
        model (class): Specifies the model class that the form interacts with.
        fields (tuple): Specifies the fields from the model to include
        in the form.

    """
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Enter title",
    }))

    image = forms.FileField()

    text = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows': "25",
        'placeholder': "Enter blog content",
    }))

    class Meta:
        """
        Metadata options for the FormBlog form.

        Attributes:
            model (class): Specifies the model class that the form interacts
            with.
            fields (tuple): Specifies the fields from the model to include in
            the form.

        """
        model = Blog
        fields = ('category', 'title', 'image', 'text')


class FormBlogImage(forms.ModelForm):
    """
    Form for creating and updating BlogImage instances.

    This form provides a field for the user to upload an image for a blog post.

    Attributes:
        image (FileField): Field for uploading an image for the blog post.

    Meta:
        model (class): Specifies the model class that the form interacts with.
        fields (tuple): Specifies the fields from the model to include in
        the form.

    """
    image = forms.FileField()

    class Meta:
        """
        Metadata options for the FormBlogImage form.

        Attributes:
            model (class): Specifies the model class that the form
            interacts with.
            fields (tuple): Specifies the fields from the model to include in
            the form.

        """
        model = BlogImage
        fields = ('image', )


BlogImageFormSet = inlineformset_factory(
    Blog, BlogImage, form=FormBlogImage,
    extra=1, can_delete=True, can_delete_extra=True
)
