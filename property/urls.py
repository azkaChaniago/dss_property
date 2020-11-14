from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', login_client, name="login_client"),
    path('logout/', logout_client, name="logout_client"),
    path('register/', register_client, name="register_client"),
    path('', home, name="home"),
    path('estate_list/', estate_list, name="estate_list"),
    path('estate_detail/<int:pk>/', estate_detail, name="estate_detail"),
    path('purchase_form/', purchase_form, name="purchase_form"),
    path('purchase_form/<int:pk>/', purchase_form, name="purchase_form"),
    path('get_detail_purchasement/<int:pk>/', get_detail_purchasement, name="get_detail_purchasement"),
    path('criteria/', criteria, name="criteria"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)