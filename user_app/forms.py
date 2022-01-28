from django import forms
from .models import Contact


class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'type': "text", 'name': "name", 'id': "name", 'class': "form-control", 'placeholder': "Введіть ім'я",
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'type': "text", 'name': "email", 'id': "email", 'class': "form-control", 'placeholder': "Введіть Email",
    }))

    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'type': "text", 'name': "subject", 'id': "subject", 'class': "form-control", 'placeholder': "Введіть тему повідомлення",
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'name': "message", 'id': "message", 'cols': "30", 'rows': "7", 'class': "form-control", 'placeholder': "Введіть повідомлення",
    }))

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
