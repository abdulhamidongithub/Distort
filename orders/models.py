from django.db import models
from django.utils import timezone

from products.models import Product
from customers.models import CustomerStore
from users.models import CustomUser
from warehouses.models import Warehouse, WarehouseProduct


STATUSES = [
    ("Active", "Active"),
    ("InProgress", "InProgress"),
    ("Delivered", "Delivered"),
    ("Confirmed", "Confirmed"),
    ("Cancelled", "Cancelled"),
]

class Order(models.Model):
    customer = models.ForeignKey(CustomerStore, on_delete=models.SET_NULL, null=True)
    operator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="operator_orders")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="driver_orders")
    sum = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    final_price = models.IntegerField(default=0)
    deadline = models.DateTimeField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUSES, default="Active")

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if self.pk and self.items.exists():
            self.sum = sum(item.tot_price for item in self.items.all())
            self.final_price = self.sum - self.discount
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    warehouse_product = models.ForeignKey(WarehouseProduct, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    tot_price = models.IntegerField()

    def save(self, *args, **kwargs):
        self.tot_price = self.amount * self.warehouse_product.product.price
        super(OrderItem, self).save(*args, **kwargs)


class KPIEarning(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('order', 'user')
