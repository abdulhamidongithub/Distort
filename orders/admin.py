from django.contrib import admin

from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "customer", "operator", "driver", "warehouse"]
    list_filter = ["status", "warehouse", "product", "customer", "driver", "operator"]
    search_fields = ["status", "warehouse", "product", "customer", "driver", "operator"]
    list_per_page = 30
    autocomplete_fields = ["customer"]

class KPIEarningAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "user", "amount"]
    list_filter = ["order", "user"]
    search_fields = ["order", "user", "amount"]
    list_per_page = 30
    autocomplete_fields = ["user"]

admin.site.register(Order, OrderAdmin)
admin.site.register(KPIEarning, KPIEarningAdmin)
