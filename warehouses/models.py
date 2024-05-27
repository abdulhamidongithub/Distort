from django.db import models
import uuid
from products.models import Product

class Warehouse(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    location = models.JSONField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, default="active")
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, {self.address}"

    class Meta:
        ordering = ["name", "id"]

class WarehouseProduct(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    invalids_amount = models.IntegerField(default=0)
    archived = models.BooleanField(default=False)
    total_sum = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.product:
            self.total_sum = self.product.price * self.amount
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('warehouse', 'product')

class WarehouseProductArrival(models.Model):
    warehouse_product = models.ForeignKey(WarehouseProduct, on_delete=models.CASCADE)
    amount = models.IntegerField()
    invalids_amount = models.IntegerField(default=0)
    comment = models.TextField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

