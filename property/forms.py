import logging
from django import forms
from django.forms import TextInput, Textarea, IntegerField, FloatField, DecimalField
from django.contrib.auth.models import User
from .models import Customer, Estate, Profession, Purchase, EstateDetails

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
    password_repeat = forms.CharField(
        label='Ulang Password',
        max_length=255,
        widget=forms.PasswordInput
    )
    
    def clean(self):
        cleaned_data = super(CustomerForm, self).clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        
        if password != password_repeat:
            message = "password and password_repeat does not match!"
            logging.warning(message)
            raise forms.ValidationError(message)

class EstateForm(forms.ModelForm):
    class Meta:
        model = Estate
        exclude = ["name", "picture", "description", "locations"]


class EstateSearchForm(forms.Form):
    lot_type = forms.CharField(
        label='Tipe Rumah',
        max_length=100
    )
    start_price = forms.DecimalField(
        label='Harga Awal',
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "type": "number",
                "step": 0.01
            }
        )
    )
    end_price = forms.DecimalField(
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

class CriteriaForm(forms.Form):
    LOAN_STATE = (
        ("0", "-"),
        ("1", "Approval"),
        ("2", "Penalty"),
        ("3", "In Arrears"),
        ("4", "Paid Off"),
    )

    address = forms.CharField(
        label='Alamat',
        max_length=255
    )
    phone = forms.CharField(
        label='No Telepon / HP',
        max_length=100,
    )
    job_ktp = forms.ModelChoiceField(
        label="Pekerjaan KTP",
        queryset=Profession.objects.all()
    )
    # job = forms.CharField(
    #     label="Pekerjaan",
    #     max_length=100
    # )
    salary = forms.IntegerField(
        label="Gaji / Upah",
    )
    on_loan = forms.BooleanField(
        label="Pinjaman"
    )
    loan_state = forms.ChoiceField(
        label="Status Angsuran",
        choices=LOAN_STATE,
        required=False
    )
    start_budget = forms.DecimalField(
        label="Harga Awal",
        widget=forms.TextInput
    )
    end_budget = forms.DecimalField(
        label="Harga Akhir",
        widget=forms.TextInput
    )

