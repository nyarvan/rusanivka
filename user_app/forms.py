import re
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

    email = forms.EmailField(
        error_messages={
            'invalid': 'Будь ласка, введіть дійсну адресу електронної пошти.'
        },
        widget=forms.TextInput(
            attrs={
                'class': "form-control", 'placeholder': "Email",
            }
        )
    )

    phone_number = forms.CharField(
        max_length=18,
        widget=forms.TextInput(
            attrs={
                'class': "form-control", 'placeholder': "Введіть номер телефону",
            }
        )
    )

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
        fields = ('name', 'email', 'phone_number', 'subject', 'message')

    def clean_name(self):
        """
        Validate and clean the user's name input.

        This method checks if the name field is not empty and matches
        the expected format. If the name is empty, it adds an error
        indicating that the name is required. If the name contains
        invalid characters (anything other than letters, spaces,
        and hyphens), it adds an error with a relevant message.

        Returns:
            str: The cleaned name if it is valid; otherwise, it returns
            the original input with errors added to the form.

        Raises:
            ValidationError: If the name does not meet the specified criteria.
        """
        name = self.cleaned_data.get('name')

        if not name:
            self.add_error('name', 'Поле вашого імені обовʼязкове.')
            return name

        if not re.match(r'^[A-Za-zА-Яа-яЁёІіЄєЇї\-\s]+$', name):
            self.add_error('name', 'Імʼя користувача має тільки літери, прогалини та дефіси.')
            return name

        return name

    def clean_phone_number(self):
        """
        Validate and clean the user's phone number input.

        This method removes all non-numeric characters from the phone number
        and checks if it starts with '0' and contains exactly 10 digits.
        If so, it prepends the country code '38' to the number. It then
        validates the length and format of the cleaned number,
        adding an error if the format is incorrect. The final format
        will be '+38(0XX) XXX XX-XX'.

        Returns:
            str: The formatted phone number if valid; otherwise, it returns
            the original input with errors added to the form.

        Raises:
            ValidationError: If the phone number does not meet the expected
            format or length.
        """
        phone = self.cleaned_data['phone_number']

        phone_cleaned = re.sub(r'\D', '', phone)

        if phone_cleaned.startswith('0') and len(phone_cleaned) == 10:
            phone_cleaned = '38' + phone_cleaned

        if not phone_cleaned.startswith('38') or len(phone_cleaned) != 12:
            self.add_error('phone_number', "Неправильний формат номеру телефону. Використовуйте формат: '+38(0XX) XXX XX-XX'.")
            return phone

        formatted_phone = f'+38(0{phone_cleaned[3:5]}) {phone_cleaned[5:8]} {phone_cleaned[8:10]}-{phone_cleaned[10:]}'
        return formatted_phone
