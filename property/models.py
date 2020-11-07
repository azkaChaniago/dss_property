from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    salary = models.FloatField(
        default=0.00,
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
    start_budget = models.FloatField(
        default=0.00,
        verbose_name="Harga Awal",
        blank=True,
        null=True
    )
    end_budget = models.FloatField(
        default=0.00,
        verbose_name="Harga Akhir",
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
    price = models.FloatField(verbose_name="Harga")
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
        choices=PROPERTY_STATE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"[{self.lot_type}] {self.name}"


class EstateDetails(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    down_payment = models.FloatField(
        default=0.00, blank=True, null=True
    )
    tenor = models.IntegerField(
        default=0, blank=True, null=True
    )
    installment = models.FloatField(
        default=0.00, blank=True, null=True
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

    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    image_type = models.CharField(max_length=50, choices=IMAGE_TYPES, default="")
    image = models.ImageField(verbose_name="Gambar", upload_to="media/")
    description = models.CharField(
        max_length=100, verbose_name="Deskripsi"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.description} ({self.estate})"


class EstateAmenity(models.Model):
    estate = models.ManyToManyField(Estate)
    name = models.CharField(default="", max_length=50)

    def __str__(self):
        return f"{self.estate.name} {self.name}"
