from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserRegistrationForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть логін",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': "password", 'class': "form-control", 'placeholder': "Введіть пароль",
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': "password", 'class': "form-control", 'placeholder': "Введіть повторно пароль",
    }))

    def clean_password2(self, *args, **kwargs):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password']

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control", 'placeholder': "Введіть логін",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': "password", 'class': "form-control", 'placeholder': "Введіть пароль",
    }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if password and username:
            user = authenticate(username=username, password=password)
            if not user or (not user.check_password(password)):
                raise forms.ValidationError('Неверный пароль или логин')
        return super().clean()
