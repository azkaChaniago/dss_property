import logging
from .forms import LoginForm
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect

def login_client(request):
    """
    docstring
    """
    templates = "login.html"
    context = {
        "title": "Login",
        "menu": "login_menu",
    }
    
    if request.method == "POST":
        logging.info("authenticating..")
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                try:
                    login(request, user)
                    logging.info(f"Login {username} success")
                    return redirect("home")
                except Exception as err:
                    logging.error(str(err))
            else:
                message = f"User {username} tidak aktif"
                logging.warning(message)
                context["message"] = message
            
    else:
        context["form"] = LoginForm()

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