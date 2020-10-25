from django.shortcuts import render

def home(request):
    """
    docstring
    """
    templates = "home.html"
    context = {
        "title": "Welcome",
        "menu": "home_menu"
    }
    return render(request, templates, context)
