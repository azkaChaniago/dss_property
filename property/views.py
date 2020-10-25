import logging
from .forms import LoginForm
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect, reverse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def login_client(request):
    """
    docstring
    """
    if request.user.is_authenticated:
        return redirect(reverse("home"))
        
    templates = "login.html"
    context = {
        "title": "Login",
        "menu": "login_menu",
    }
    
    if request.method == "POST":
        logger.info("authenticating..")
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info(f"Login {username} success")
                    return redirect("home")
                else:
                    message = f"{username} tidak aktif"
                    logger.warning(message)
                    context["message"] = message
                    context["form"] = LoginForm()
            else:
                message = f"User {username} gagal login"
                logger.warning(message)
                context["message"] = message
                context["form"] = LoginForm()
    else:
        context["form"] = LoginForm()

    return render(request, templates, context)


def home(request):
    """
    docstring
    """
    logger.info(f"{request.user} mencoba masuk")
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