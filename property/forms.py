from django import forms
from django.forms import TextInput, Textarea, IntegerField, FloatField
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
        exclude = ["name", "picture", "description", "locations"]


class EstateSearchForm(forms.Form):
    lot_type = forms.CharField(
        label='Tipe Rumah',
        max_length=100
    )
    start_price = forms.FloatField(
        label='Harga Awal',
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "type": "number",
                "step": 0.01
            }
        )
    )
    end_price = forms.FloatField(
        label='Harga Akhir',
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "type": "number",
                "step": 0.01
            }
        )
    )
    bedroom = forms.IntegerField(
        label="Jumlah Kamar Tidur",
        min_value=1,
        widget=forms.TextInput(
            attrs={
                "type": "number",
                "step": 1
            }
        )
    )
    bathroom = forms.IntegerField(
        label="Jumlah Kamar Mandi",
        min_value=1,
        widget=forms.TextInput(
            attrs={
                "type": "number",
                "step": 1
            }
        )
    )
