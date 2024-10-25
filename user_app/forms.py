from django import forms
from .models import Contact


class FormContact(forms.ModelForm):
    """
    Form for contacting.

    Attributes:
        name (str): The name of the contact.
        email (Email): The email address of the contact.
        subject (str): The subject of the message.
        message (str): The message content.
    """

    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "ПІБ",
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Email",
    }))

    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Тема",
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'cols': "30", 'rows': "7",
        'class': "form-control", 'placeholder': "Повідомлення",
    }))

    class Meta:
        """
        Meta options for the FormContact form.

        Attributes:
            model (Model): The model that the form is associated with.
            fields (tuple): The fields of the model to include in the form.
        """
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
