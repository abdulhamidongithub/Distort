from django.contrib import admin

from .models import *

class CustomerStoreAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "address", "warehouse"]
    list_display_links = ["name"]
    list_editable = ["phone", "address"]
    list_filter = ["warehouse", "status"]
    search_fields = ["name", "phone", "address", "warehouse"]
    list_per_page = 30

admin.site.register(CustomerStore, CustomerStoreAdmin)

