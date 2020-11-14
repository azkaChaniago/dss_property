import logging
from .utilities import get_recomendation, calc_loan_weight
from .forms import LoginForm, CustomerForm, EstateSearchForm, CriteriaForm
from .models import Customer, Estate, EstateDetails, EstateGallery, Purchase
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
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

    if not customer.job_ktp or not customer.salary or not customer.loan_state:
        return redirect("criteria")
    
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
    estates = Estate.objects.filter(pk__in=recomendations)
    context = {
        "title": "Welcome",
        "menu": "home_menu",
        "estates_slides": estates[:3],
        "estates": estates,
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
            email = form.cleaned_data.get("email")
            user = User.objects.filter(
                email=email
            ).first()

            if not user:
                username = fullname.lower().replace(" ", "_")
                splited_name = fullname.split()
                first_name = splited_name[0]
                last_name = splited_name[-1] if len(splited_name) > 1 else ""
                password = form.cleaned_data.get("password")

                try:
                    user = User(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email
                    )
                    user.set_password(password)
                    user.save()
                except Exception as err:
                    logging.error(str(err))
                    context["message"] = "Terjadi kesalahan pada saat mendaftarkan user!"
                    context["status"] = "error"
            
            try:
                customer = Customer(
                    user=user,
                    fullname=fullname
                )
                customer.save()

                authenticate(
                    username=username, password=password
                )
                return redirect("login_client")
            except Exception as err:
                logging.error(str(err))
                context["message"] = "Terjadi kesalahan pada saat mendaftarkan customer!"
                context["status"] = "error"
            
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
        "estate_forms": EstateSearchForm(),
        "estate_gallery": estate.estategallery_set.all(),
        "estate_amenity": estate.estateamenity_set.all(),
        "estate_details": estate.estatedetails_set.all(),
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
        lot_type = f"Tipe {request.GET.get('type')}"
        filters.update({ "lot_type": lot_type })

    if filters:
        estate = estate.filter(**filters)
    
    paginator = Paginator(estate, 3)

    page = request.GET.get("page")
    estate = paginator.get_page(page)

    context.update({
        "title": "Hasil Pencarian",
        "estates": estate
    })
    
    return render(request, templates, context)


def purchase_form(request, pk=None):
    customer = request.user.customer
    estate = get_object_or_404(Estate, pk=pk)
    purchase = Purchase.objects.filter(
        customer_id=customer.pk,
        estate_id=estate.pk,
        state="draft"
    ).first()

    templates = "purchase/purchase_form.html"
    context = {
        "title": "Form Pembelian",
        "menu": "purchase_form_menu",
        "estate": estate,
        "customer": customer,
        "estate_details": estate.estatedetails_set.all(),
        "purchase": purchase,
    }

    if request.POST:
        if purchase:
            if not request.FILES.get("proof"):
                logger.warning("Payment Proof is not uploaded!")
            purchase.proof = request.FILES.get("proof")
            purchase.state = "paid"
            purchase.save()

            estate.state = "sold"
            estate.save()
        else:
            purchase_state = "draft"
            estate_state = "booked"
            if request.FILES.get("proof"):
                purchase_state = "paid"
                estate_state = "sold"
            
            dp_id = request.POST.get("down_payment")
            estate_detail = EstateDetails.objects.get(pk=dp_id)

            purchase = Purchase(
                customer=customer,
                estate=estate,
                proof=request.FILES.get("proof"),
                down_payment_id=estate_detail,
                down_payment=estate_detail.down_payment,
                tenor=estate_detail.tenor,
                installments=estate_detail.installment,
                state=purchase_state
            )
            purchase.save()

            estate.state = estate_state
            estate.save()
        return redirect("estate_detail", pk=estate.pk)

    return render(request, templates, context)

def get_detail_purchasement(request, pk):
    try:
        detail = EstateDetails.objects.get(pk=pk)
        response = {
            "tenor": detail.tenor,
            "installments": detail.installment,
        }
    except Exception as err:
        logger.error(err)
        response = {
            "tenor": 0,
            "installments": 0.00,
        }

    return JsonResponse(response, safe=False)


def criteria(request):

    if not request.user.is_authenticated:
        return redirect("login_client")
    
    customer = request.user.customer
    templates = "criteria.html"
    context = {
        "title": "Kriteria",
        "menu": "criteria_menu",
        "customer": customer,
        "form": CriteriaForm(instance=customer)
    }
    
    if request.POST:
        form = CriteriaForm(request.POST, instance=customer)
        if form.is_valid():
            try:
                customer.address = form.cleaned_data.get("address")
                customer.phone = form.cleaned_data.get("phone")
                customer.job_ktp = form.cleaned_data.get("job_ktp")
                customer.salary = form.cleaned_data.get("salary")
                customer.on_loan = form.cleaned_data.get("on_loan")
                customer.loan_state = form.cleaned_data.get("loan_state")
                customer.start_budget = form.cleaned_data.get("start_budget")
                customer.end_budget = form.cleaned_data.get("end_budget")
                customer.save()

                return redirect("home")
            except Exception as err:
                logging.error(err)
                context["message"] = "Terjadi kesalahan saat menyimpan data!"
                context["state"] = "error"

    return render(request, templates, context)


def about(request):
    templates = "about.html"
    context = {
        "title": "Tentang Kami",
        "menu": "about_menu",
    }

    return render(request, templates, context)