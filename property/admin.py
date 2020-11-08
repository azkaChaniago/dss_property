from django.contrib import admin
from .models import *

class EstateDetailInline(admin.TabularInline):
    model = EstateDetails
    extra = 0


class EstateGalleryInline(admin.TabularInline):
    model = EstateGallery
    extra = 0


class EstateAmenityInline(admin.TabularInline):
    model = EstateAmenity
    extra = 0


class EstateAdmin(admin.ModelAdmin):
    list_display = ("__str__", "locations", "state")
    list_filter = ("state", "lot_type")
    list_per_page = 10
    empty_value_display = "-kosong-"
    fields = (
        "name",
        "lot_type",
        ("bathroom", "lot_length"),
        ("bedroom", "lot_width"),
        ("state", "price"),
        "picture",
        "locations",
        "description"
    )

    inlines = [
        EstateDetailInline, EstateGalleryInline, EstateAmenityInline
    ]
    
admin.site.register(Estate, EstateAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("__str__", "address", "phone")
    list_filter = ("loan_state", "job_ktp")
    list_per_page = 10
    empty_value_display = "-kosong-"
    
admin.site.register(Customer, CustomerAdmin)
