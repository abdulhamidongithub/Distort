from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "status"]
    list_display_links = ["id", "name"]
    list_editable = ["status"]
    list_filter = ["status"]
    search_fields = ["name", "status"]
    list_per_page = 30

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", 'category']
    list_display_links = ["name"]
    list_editable = ["price"]
    list_filter = ["category"]
    search_fields = ["category", "name"]
    list_per_page = 30

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
