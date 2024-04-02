from django.contrib import admin

from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "phone_number","role", "warehouse"]
    list_display_links = ["id", "first_name"]
    list_editable = ["role", "phone_number"]
    list_filter = ["role", "warehouse"]
    search_fields = ["first_name", "last_name", "phone_number"]
    list_per_page = 30

class CarAdmin(admin.ModelAdmin):
    list_display = ["id", "driver", "type", 'number']
    list_display_links = ["driver"]
    list_editable = ["type", "number"]
    list_filter = ["type", "driver"]
    search_fields = ["driver", "number"]
    list_per_page = 30

class SalaryParamsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "fixed", 'kpi_by_sales']
    list_editable = ["fixed", "kpi_by_sales"]
    list_filter = ["user"]
    search_fields = ["user"]
    list_per_page = 30

class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "payer", 'amount', "paid_at"]
    list_filter = ["user", "payer"]
    search_fields = ["user", "payer", "paid_at"]
    list_per_page = 30

class TaskAdmin(admin.ModelAdmin):
    list_display = ["task", "task_setter", "task_executors", 'status', "deadline"]
    list_editable = ["status", "deadline"]
    list_filter = ["task_setter", "task_executors", "status"]
    search_fields = ["task_setter", "task_executors", "deadline"]
    list_per_page = 30

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(SalaryParams, SalaryParamsAdmin)
admin.site.register(SalaryPayment, SalaryPaymentAdmin)
admin.site.register(Task, TaskAdmin)
