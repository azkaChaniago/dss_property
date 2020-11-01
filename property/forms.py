from django import forms
from django.contrib.auth.models import User
from .models import Customer, Estate, Profession

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
    LOAN_STATE = (
        ("1", "Approval"),
        ("2", "Penalty"),
        ("3", "In Arrears"),
        ("4", "Paid Off"),
    )
    
    email = forms.CharField(
        label='Alamat email',
        max_length=100
    )
    fullname = forms.CharField(
        label='Nama Lengkap',
        max_length=100
    )
    password = forms.CharField(
        label='Password',
        max_length=255,
        widget=forms.PasswordInput
    )
    address = forms.CharField(
        label='Alamat',
        max_length=100,
        widget=forms.TextInput()
    )
    phone = forms.CharField(
        label='No Telepon / HP',
        max_length=100,
    )
    job_ktp = forms.ModelMultipleChoiceField(
        queryset=Profession.objects.all()
    )
    job = forms.CharField(
        label="Pekerjaan",
        max_length=100
    )
    salary = forms.IntegerField(
        label="Gaji / Upah",
    )
    on_loan = forms.BooleanField()
    loan_state = forms.ChoiceField(
        label="Status Angsuran",
        choices=LOAN_STATE
    )


class EstateForm(forms.ModelForm):
    class Meta:
        model = Estate
        fields = [
            "name", "lot_type", "lot_length", "lot_width",
            "price", "description", "locations", "picture",
            "bedroom", "bathroom"
        ]