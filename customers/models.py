from django.db import models
import uuid
from warehouses.models import Warehouse
from users.models import CustomUser

class CustomerStore(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    long = models.CharField(max_length=100, null=True, blank=True)
    lat = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=30, default="active")
    created_at = models.DateField(auto_now_add=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}, {self.address}"

    class Meta:
        ordering = ["name", "address"]
