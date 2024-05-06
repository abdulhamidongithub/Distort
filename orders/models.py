from django.db import models
from django.utils import timezone

from products.models import Product
from customers.models import CustomerStore
from users.models import CustomUser
from warehouses.models import Warehouse, WarehouseProduct


STATUSES = [
    ("Active", "Active"),
    ("Delivered", "Delivered"),
    ("Confirmed", "Confirmed"),
    ("Cancelled", "Cancelled"),
]

class Order(models.Model):
    product = models.ForeignKey(WarehouseProduct, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(CustomerStore, on_delete=models.SET_NULL, null=True)
    operator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="operator_orders")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="driver_orders")
    amount = models.IntegerField()
    total_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    deadline = models.DateTimeField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices=STATUSES,
        default="Active"
    )

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.total_price:  # If total_price is not provided explicitly
            if self.product:  # Ensure product is set
                product_price = self.product.product.price
                self.total_price = (self.amount * product_price) - self.discount
        super().save(*args, **kwargs)

class KPIEarning(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)

