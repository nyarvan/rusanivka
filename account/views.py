from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegistrationForms


def login_view(request):
    """
    View function for user login.

    This view handles user authentication and redirects the user to the
    next page after successful login.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the next page after successful
        login, or redirects to the home page if no next page is provided.

    """
    form = UserLoginForm(request.POST or None)
    next_page = request.GET.get('next')

    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username.strip(), password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        return redirect(next_post or next_page or '/')

    return render(request, 'login.html', context={'form': form})


def logout_view(request):
    """
    View function for user logout.

    This view logs out the current user and redirects to the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the home page after logout.

    """
    logout(request)
    return redirect('/')


def registration_view(request):
    """
    View function for user registration.

    This view handles user registration by saving a new user to the database
    after form validation.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the registration form or registration
        success page.

    """
    form = UserRegistrationForms(request.POST or None)

    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return render(request, 'reg_done.html', context={'new_user': new_user})

    return render(request, 'registration.html', context={'form': form})
