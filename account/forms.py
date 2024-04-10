from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserRegistrationForms(forms.ModelForm):
    """
    Form class for user registration.

    This form handles user registration by taking the user's desired
    username and password, ensuring that the passwords match.

    Attributes:
        username (CharField): Field for entering the desired username.
        password (CharField): Field for entering the password.
        password2 (CharField): Field for entering the password again for
        confirmation.

    """

    class Meta:
        """
        Metadata class for the form.

        This class specifies the model and fields to be used for the form.

        Attributes:
            model (Model): The user model to use for registration.
            fields (tuple): The fields from the model to include in the form.

        """
        model = User
        fields = ('username',)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Введіть логін",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'placeholder': "Введіть пароль",
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'placeholder': "Введіть повторно пароль",
    }))

    def clean_password2(self):
        """
        Method to validate password confirmation.

        This method ensures that the entered passwords match.

        Returns:
            str: The validated password.

        Raises:
            forms.ValidationError: If the passwords do not match.

        """
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password']


class UserLoginForm(forms.Form):
    """
    Form class for user login.

    This form handles user login by taking the user's username and password,
    validating them, and authenticating the user.

    Attributes:
        username (CharField): Field for entering the username.
        password (CharField): Field for entering the password.

    """

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Введіть логін",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'placeholder': "Введіть пароль",
    }))

    def clean(self):
        """
        Method to clean and validate form data.

        This method validates the entered username and password by
        authenticating the user.
        If the authentication fails, it raises a ValidationError.

        Returns:
            dict: Cleaned form data.

        Raises:
            forms.ValidationError: If the authentication fails due to
            incorrect username or password.

        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if password and username:
            user = authenticate(username=username, password=password)
            if not user or (not user.check_password(password)):
                raise forms.ValidationError('Неверный пароль или логин')
        return super().clean()
