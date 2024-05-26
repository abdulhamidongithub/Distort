from django.contrib import admin
from .models import Order, KPIEarning, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "operator", "warehouse", "driver", "status", "date_time"]
    list_filter = ["status", "warehouse", "customer", "operator"]
    search_fields = ["status", "warehouse__name", "customer__name", "operator__username"]
    list_per_page = 30
    autocomplete_fields = ["customer", "warehouse", "driver", "operator"]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "warehouse_product", "amount", "tot_price"]
    list_filter = ["order__status", "warehouse_product__warehouse"]
    search_fields = ["order__id", "warehouse_product__product__name"]
    list_per_page = 30
    autocomplete_fields = ["order", "warehouse_product"]

class KPIEarningAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "user", "amount"]
    list_filter = ["order", "user"]
    search_fields = ["order__id", "user__username", "amount"]
    list_per_page = 30
    autocomplete_fields = ["order", "user"]

admin.site.register(Order, OrderAdmin)
admin.site.register(KPIEarning, KPIEarningAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
