from django.shortcuts import render, redirect
from .foms import UserLoginForm, UserRegistrationForms
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next = request.GET.get('next')

    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username.strip(), password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        return redirect(next_post or next or '/')

    return render(request, 'login.html', context={
        'form': form,
    })


def logout_view(request):
    logout(request)
    return redirect('/')


def registration_view(request):
    form = UserRegistrationForms(request.POST or None)

    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return render(request, 'reg_done.html', context={'new_user': new_user})

    return render(request, 'registration.html', context={'form': form})
