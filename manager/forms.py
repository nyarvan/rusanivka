from django import forms
from django.forms import inlineformset_factory
from user_app.models import Administration, Doctor, Department, CategoryBlog, Blog, BlogImage


class FormAdministration(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть ПІБ",
    }))

    position = forms.DecimalField(widget=forms.TextInput(attrs={
        'type': "number", 'class': "form-control", 'placeholder': "Введіть позицію",
    }))

    image = forms.FileField()

    post = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть посаду",
    }))

    schedule = forms.CharField(widget=forms.Textarea(attrs={
        'type': "text", 'class': "form-control", 'rows': "5", 'placeholder': "Введіть графік роботи",
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть номер телефону",
    }))

    class Meta:
        model = Administration
        fields = ('name', 'position', 'image', 'post', 'schedule', 'phone')


class FormDoctor(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть ПІБ",
    }))

    image = forms.FileField(required=False)

    post = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть посаду",
    }))

    room = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть кабінет",
    }))

    schedule = forms.CharField(widget=forms.Textarea(attrs={
        'type': "text", 'class': "form-control", 'rows': "5", 'placeholder': "Введіть графік роботи",
    }))

    class Meta:
        model = Doctor
        fields = ('department', 'name', 'image', 'post', 'room', 'schedule', 'is_manager', 'is_visible')


class FormDepartment(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть назву закладу",
    }))

    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть повну назву закладу",
    }))

    number = forms.DecimalField(widget=forms.TextInput(attrs={
        'type': "number", 'class': "form-control", 'placeholder': "Введіть номер закладу",
    }))

    manager = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть ПІБ завідувача",
    }))

    image = forms.FileField()

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть номер телефону",
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть адресу закладу",
    }))

    class Meta:
        model = Department
        fields = ('name', 'full_name', 'number', 'manager', 'image', 'phone', 'address')


class FormBlog(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть заголовок",
    }))

    image = forms.FileField()

    text = forms.CharField(widget=forms.Textarea(attrs={
        'type': "text", 'class': "form-control", 'rows': "25", 'placeholder': "Введіть текст новини",
    }))

    class Meta:
        model = Blog
        fields = ('title', 'image', 'text')


class FormBlogImage(forms.ModelForm):

    image = forms.FileField()

    class Meta:
        model = BlogImage
        fields = ('image', )


BlogImageFormSet = inlineformset_factory(
    Blog, BlogImage, form=FormBlogImage,
    extra=1, can_delete=True, can_delete_extra=True
)
