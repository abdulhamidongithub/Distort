from django.contrib import admin

from .models import *

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "address"]
    list_display_links = ["id", "name"]
    list_editable = ["address", "phone"]
    list_filter = ["status"]
    search_fields = ["name", "phone", "address"]
    list_per_page = 30

class WarehouseProductAdmin(admin.ModelAdmin):
    list_display = ["id", "warehouse", "product", "amount", "invalids_amount"]
    list_editable = ["amount", "invalids_amount"]
    list_filter = ["warehouse", "product"]
    search_fields =["warehouse", "product"]
    list_per_page = 30

admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(WarehouseProduct, WarehouseProductAdmin)

