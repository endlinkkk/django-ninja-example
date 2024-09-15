from django.contrib import admin

from core.apps.customers.models import Customer


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "created_at")
    search_fields = [
        "phone",
    ]
