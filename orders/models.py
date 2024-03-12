from django.db import models
from products.models import Product
from customers.models import CustomerStore
from users.models import CustomUser
from warehouses.models import Warehouse

STATUSES = [
    ("Accepted", "Accepted"),
    ("Processing", "Processing"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
]

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(CustomerStore, on_delete=models.SET_NULL, null=True)
    operator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="operator_orders")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="driver_orders")
    amount = models.IntegerField()
    deadline = models.DateTimeField()
    date_time = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices=STATUSES,
        default="Accepted"
    )

    class Meta:
        ordering = ["-id"]
