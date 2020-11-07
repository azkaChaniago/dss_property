import logging
from .forms import LoginForm, CustomerForm, EstateSearchForm
from .models import Customer, Estate, EstateDetails, EstateGallery
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse, get_object_or_404

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
        "estates": Estate.objects.all().order_by('created_at', 'name'),
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
        "form": CustomerForm()
    }
    
    if request.method == "POST":
        logger.info("authenticating..")
        form = CustomerForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data.get("fullname")
            user = User.objects.filter(
                email=form.cleaned_data.get("email")
            ).first()
            if not user:
                username = fullname.lower().replace(" ", "_")
                user = User(
                    username=username,
                    email=form.cleaned_data.get("email"),
                    password = form.cleaned_data.get("password")
                )
                user.save()

            customer = Customer(
                user=user,
                fullname=form.cleaned_data.get("fullname"),
                address=form.cleaned_data.get("address"),
                phone=form.cleaned_data.get("phone"),
                job_ktp=form.cleaned_data.get("job_ktp"),
                job=form.cleaned_data.get("job"),
                salary=form.cleaned_data.get("salary"),
                on_loan=form.cleaned_data.get("on_loan"),
                loan_state=form.cleaned_data.get("loan_state"),
                start_budget=form.cleaned_data.get("start_budget"),
                end_budget=form.cleaned_data.get("end_budget")
            )
            customer.save()
            return redirect("login")

    return render(request, templates, context)
    

def estate_detail(request, pk):
    """
    docstring
    """
    estate = get_object_or_404(Estate, pk=pk)

    logger.info(f"{request.user} mencoba masuk")
    templates = "estate/estate_detail.html"
    context = {
        "title": "Detail Rumah",
        "menu": "estate_detail_menu",
        "estate": estate,
        # "estate_forms": EstateSearchForm()
    }
    
    # if request.POST:
    #     form = EstateSearchForm(request.POST)
    #     filters = {}
    #     if form.is_valid():
    #         lot_type = form.cleaned_data.get("lot_type")
    #         if lot_type:
    #             filters.update({ "lot_type__iexact": lot_type })
    #         bedroom = form.cleaned_data.get("bedroom")
    #         if bedroom:
    #             filters.update({ "bedroom": bedroom })
    #         bathroom = form.cleaned_data.get("bathroom")
    #         if bathroom:
    #             filters.update({ "bathroom": bathroom })
    #         start_price = form.cleaned_data.get("start_price")
    #         end_price = form.cleaned_data.get("end_price")
    #         if start_price and end_price:
    #             filters.update({"price__range": (start_price, end_price) })
            
    #         estate = Estate.objects.filter(**filters)
    #         context["query_results"] = estate

    return render(request, templates, context)
