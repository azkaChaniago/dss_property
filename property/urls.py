from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', login_client, name="login_client"),
    path('logout/', logout_client, name="logout_client"),
    path('register/', register_client, name="register_client"),
    path('', home, name="home"),
    path('estate_detail/<int:pk>/', estate_detail, name="estate_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)