import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profession(models.Model):
    profession = models.CharField(
        max_length=100, verbose_name="Pekerjaan", default=""
    )
    weight = models.FloatField(
        default=0.00, verbose_name="Bobot Nilai"
    )

    def __str__(self):
        return self.profession


class Customer(models.Model):
    # temporary state, should be modified
    LOAN_STATE = (
        ("0", "-"),
        ("1", "Approval"),
        ("2", "Penalty"),
        ("3", "In Arrears"),
        ("4", "Paid Off"),
    )
    # available jobs in KTP, should using own table

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Akun"
    )
    address = models.TextField(verbose_name="Alamat")
    phone = models.CharField(
        max_length=20, verbose_name="No Telepon / HP"
    )
    fullname = models.CharField(
        max_length=100, verbose_name="Nama"
    )
    job_ktp = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        verbose_name="Pekerjaan (KTP)",
        blank=True,
        null=True
    )
    job = models.CharField(
        max_length=100,
        default="",
        verbose_name="Pekerjaan",
        null=True,
        blank=True
    )
    salary = models.DecimalField(
        default=0.00,
        max_digits=15,
        decimal_places=2,
        verbose_name="Gaji",
        blank=True,
        null=True
    )
    on_loan = models.BooleanField(
        default=False,
        verbose_name="Punya pinjaman?",
        blank=True,
        null=True
    )
    loan_state = models.CharField(
        default="",
        max_length=20,
        verbose_name="Status Pinjaman",
        choices=LOAN_STATE
    )
    start_budget = models.DecimalField(
        default=0.00,
        verbose_name="Harga Awal",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True
    )
    end_budget = models.DecimalField(
        default=0.00,
        verbose_name="Harga Akhir",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.fullname or self.user.username


class Estate(models.Model):
    PROPERTY_STATE = (
        ("available", 'Tersedia'),
        ("booked", 'Booking'),
        ("sold", 'Terjual'),
    )
    
    name = models.CharField(max_length=50, verbose_name="Nama")
    lot_type = models.CharField(
        max_length=50, verbose_name="Tipe Rumah"
    )
    lot_length = models.FloatField(verbose_name="Panjang")
    lot_width = models.FloatField(verbose_name="Lebar")
    price = models.DecimalField(
        default=0.00,
        verbose_name="Harga",
        max_digits=18,
        decimal_places=2
    )
    description = models.TextField(
        default="", verbose_name="Deskripsi"
    )
    locations = models.TextField(
        default="", verbose_name="Lokasi"
    )
    picture = models.ImageField(
        verbose_name="Gambar Thumbnail",
        null=True, blank=True, upload_to="media/"
    )
    bedroom = models.IntegerField(default=1, verbose_name="Kamar Tidur")
    bathroom = models.IntegerField(default=1, verbose_name="Kamar Mandi")
    state = models.CharField(
        default="available",
        max_length=50,
        verbose_name="Status",
        choices=PROPERTY_STATE,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"[{self.lot_type}] {self.name}"


class EstateDetails(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    down_payment = models.DecimalField(
        default=0.00,
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True
    )
    tenor = models.IntegerField(
        default=0, blank=True, null=True
    )
    installment = models.DecimalField(
        default=0.00,
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.estate.lot_type}] {self.estate.name} \
            ({self.installment}x)"


class EstateGallery(models.Model):
    IMAGE_TYPES = (
        ("cover", "Gambar Cover"),
        ("gallery", "Galeri"),
    )

    def upload_path(self, filename):
        lot_type = self.estate.lot_type.lower().replace(" ", "_")
        estate_name = self.estate.name.lower().replace(" ", "_")
        mark = self.estate.created_at.date()
        dir_name = f"{lot_type}_{estate_name}_{mark}"
        return f"media/{dir_name}/{filename}"

    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    image_type = models.CharField(
        max_length=50,
        choices=IMAGE_TYPES,
        default="",
        blank=True,
        null=True
    )
    image = models.ImageField(
        verbose_name="Gambar",
        upload_to=upload_path,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=100,
        verbose_name="Deskripsi",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.description} ({self.estate})"


class EstateAmenity(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    name = models.CharField(
        default="",
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"[ID:{self.estate.pk}] {self.estate.name} {self.name}"


class Purchase(models.Model):
    PAYMENT_STATE = (
        ("draft", "Draft"),
        ("paid", "Paid"),
        ("cancel", "Cancel"),
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="Kustomer"
    )
    estate = models.ForeignKey(
        Estate, on_delete=models.CASCADE, verbose_name="Properti"
    )
    down_payment_id = models.ForeignKey(
        EstateDetails, on_delete=models.CASCADE
    )
    down_payment = models.DecimalField(
        default=0.00,
        max_digits=18,
        decimal_places=2,
        verbose_name="Uang Muka"
    )
    state = models.CharField(
        default="draft",
        max_length=20,
        choices=PAYMENT_STATE,
        verbose_name="Status"
    )
    tenor = models.IntegerField(default=1, verbose_name="Tenor")
    installments = models.DecimalField(
        default=0.00,
        max_digits=18,
        decimal_places=2,
        verbose_name="Angsuran"
    )
    proof = models.ImageField(
        upload_to="media/payments/",
        verbose_name="Bukti Pembayaran",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        customer = self.customer.fullname.split(" ")
        customer_code = ""
        for name in customer:
            customer_code += name[0].upper()
        if len(customer_code) == 2:
            customer_code += customer[1][1].upper()
        elif len(customer_code) == 1:
            customer_code += customer[0][1].upper()
            customer_code += customer[0][2].upper()
        
        estate_code = self.estate.name.split(" ")
        estate_code = "".join([est[0].upper() for est in estate_code])

        init_date = timezone.now().strftime('%Y-%m-%d')
        init_date = init_date.replace("-", "")

        return f"{customer_code}/{estate_code}/{init_date}"
    
    def save(self, *args, **kwargs):
        if not self.customer or not self.estate:
            raise ValueError("Customer or Estate is not selected!")
        super(Purchase, self).save(*args, **kwargs)
