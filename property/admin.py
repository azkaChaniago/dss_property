from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(EstateGallery)

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
        ("lot_type", "price"),
        ("lot_length", "lot_width"),
        ("bedroom", "bathroom"),
        ("picture", "state"),
        "locations",
        "description"
    )

    inlines = [
        EstateDetailInline, EstateGalleryInline, EstateAmenityInline
    ]
    
admin.site.register(Estate, EstateAdmin)
