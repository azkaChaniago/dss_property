from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', login_client, name="login_client"),
    path('logout/', logout_client, name="logout_client"),
    path('home/', home, name="home"),
]