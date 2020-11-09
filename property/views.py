import logging
from .utilities import get_recomendation, calc_loan_weight
from .forms import LoginForm, CustomerForm, EstateSearchForm, PurchaseForm
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
    customer = request.user.customer
    
    """
    Pre-processing data and requirements
    to calculate recomendation using
    Simple Additive Weighting Algorithm
    """
    estate_range = Estate.objects.filter(
        price__gte=customer.start_budget,
        price__lte=customer.end_budget
    )
    
    criteria = []
    for est in estate_range:
        criteria.append({
            "id": est.id,
            "price": est.price,
            "job": customer.job_ktp.weight,
            "salary": customer.salary,
            "loan_state": calc_loan_weight(customer.loan_state)
        })

    recomendations = get_recomendation(criteria)
    """
    Finding calculation is finished here
    the rest is orm the recomendations id into Estate model
    """

    context = {
        "title": "Welcome",
        "menu": "home_menu",
        "estates": Estate.objects.filter(pk__in=recomendations),
        "estate_forms": EstateSearchForm()
    }

    if request.POST:
        form = EstateSearchForm(request.POST)
        params = "?search=true"
        if form.is_valid():
            lot_type = form.cleaned_data.get("lot_type")
            if lot_type:
                params += f"&lot_type={lot_type}"
            bedroom = form.cleaned_data.get("bedroom")
            if bedroom:
                params += f"&bedroom={bedroom}"
            bathroom = form.cleaned_data.get("bathroom")
            if bathroom:
                params += f"&bathroom={bathroom}"
            start_price = form.cleaned_data.get("start_price")
            end_price = form.cleaned_data.get("end_price")
            if start_price and end_price:
                params += f"&start_price={start_price}&end_price={end_price}"
            
            return redirect(f"estate_list{params}")

    return render(request, templates, context)


def logout_client(request):
    logout(request)
    return redirect("login_client")


def register_client(request):
    """
    docstring
    """
    if request.user.is_authenticated:
        return redirect("home")

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
                splited_name = fullname.split()
                first_name = splited_name[0]
                last_name = splited_name[-1] if len(splited_name) > 1 else ""
                user = User(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=form.cleaned_data.get("email")
                )
                user.set_password(form.cleaned_data.get("password"))
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
            return redirect("login_client")

    return render(request, templates, context)
    

def estate_detail(request, pk):
    """
    docstring
    """
    estate = get_object_or_404(Estate, pk=pk)

    # customer = request.user.customer
    # estate = Estate.objects.get(pk=pk)

    # PurchaseForm()

    logger.info(f"{request.user} mencoba masuk")
    templates = "estate/estate_detail.html"
    context = {
        "title": "Detail Rumah",
        "menu": "estate_detail_menu",
        "estate": estate,
        "estate_forms": EstateSearchForm(),
        "estate_gallery": estate.estategallery_set.all(),
        "estate_amenity": estate.estateamenity_set.all(),
        "estate_details": estate.estatedetails_set.all(),
        "purchase_forms": PurchaseForm()
    }

    return render(request, templates, context)


def estate_list(request):
    """
    docstring
    """
    estate = Estate.objects.all()
    templates = "estate/estate_list.html"
    context = {
        "title": "Daftar Properti",
        "menu": "estate_list_menu",
        "estates": estate,
        "estate_forms": EstateSearchForm()
    }

    filters = {}
    if request.GET.get("search"):
        if request.GET.get("lot_type"):
            filters.update({ "lot_type__iexact": request.GET.get("lot_type") })
        
        if request.GET.get("bedroom"):
            filters.update({ "bedroom": request.GET.get("bedroom") })
        
        if request.GET.get("bathroom"):
            filters.update({ "bathroom": request.GET.get("bathroom") })
        
        if request.GET.get("start_price") and request.GET.get("end_price"):
            filters.update({
                "price__range": (
                    request.GET.get("start_price"), request.GET.get("end_price")
                )
            })
    elif request.GET.get("type"):
        filters.update({ "lot_type": request.GET.get("type") })

    if filters:
        estate = estate.filter(**filters)
        context.update({
            "title": "Hasil Pencarian",
            "estates": estate
        })
    
    return render(request, templates, context)
