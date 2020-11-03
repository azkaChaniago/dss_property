import logging
from .forms import LoginForm, CustomerForm, EstateSearchForm
from .models import Estate, EstateDetails, EstateGallery
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
        "menu": "home_menu",
        "estates": Estate.objects.all(),
        "estate_forms": EstateSearchForm()
    }
    
    if request.POST:
        form = EstateSearchForm(request.POST)
        filters = {}
        if form.is_valid():
            lot_type = form.cleaned_data.get("lot_type")
            if lot_type:
                filters.update({ "lot_type__iexact": lot_type })
            bedroom = form.cleaned_data.get("bedroom")
            if bedroom:
                filters.update({ "bedroom": bedroom })
            bathroom = form.cleaned_data.get("bathroom")
            if bathroom:
                filters.update({ "bathroom": bathroom })
            start_price = form.cleaned_data.get("start_price")
            end_price = form.cleaned_data.get("end_price")
            if start_price and end_price:
                filters.update({"price__range": (start_price, end_price) })
            
            estate = Estate.objects.filter(**filters)
            context["query_results"] = estate

    return render(request, templates, context)


def logout_client(request):
    logout(request)
    return redirect("login_client")


def register_client(request):
    """
    docstring
    """
    templates = "register.html"
    context = {
        "title": "Register",
        "menu": "register_menu",
    }
    
    if request.method == "POST":
        logger.info("authenticating..")
        form_user = LoginForm(request.POST)
        form_customer = CustomerForm(request.POST)
        if form.is_valid():
            username = form_user.cleaned_data.get("username")
            password = form_user.cleaned_data.get("password")
            address = form_customer.cleaned_data.get("address")
            phone = form_customer.cleaned_data.get("phone")
            email = form_customer.cleaned_data.get("email")
            fullname = form_customer.cleaned_data.get("fullname")
            
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
        context["form_user"] = LoginForm()
        context["form_customer"] = CustomerForm()

    return render(request, templates, context)
    