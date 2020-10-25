from django import forms
from django.contrib.auth.models import User
from .models import Customer

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User


class CustomerForm(forms.Form):
    address = forms.CharField(
        label='Alamat',
        max_length=100,
        widget=forms.TextInput()
    )
    phone = forms.CharField(
        label='No Telepon / HP',
        max_length=100,
        widget=forms.PasswordInput()
    )
    email = forms.CharField(
        label='Alamat email',
        max_length=100
    )
    fullname = forms.CharField(
        label='Nama Lengkap',
        max_length=100
    )

    class Meta:
        model = Customer
