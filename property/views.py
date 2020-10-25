from django.contrib.auth import logout
from django.shortcuts import render, redirect

def login_client(request):
    """
    docstring
    """
    templates = "login.html"
    context = {
        "title": "Login",
        "menu": "login_menu"
    }
    return render(request, templates, context)


def home(request):
    """
    docstring
    """
    if not request.user.is_authenticated:
        return redirect('logout_client')

    templates = "home.html"
    context = {
        "title": "Welcome",
        "menu": "home_menu"
    }
    return render(request, templates, context)


def logout_client(request):
    logout(request)
    return redirect("login_client")