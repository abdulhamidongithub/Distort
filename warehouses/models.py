from django.db import models
import uuid
from users.models import CustomUser
from products.models import Product

class Warehouse(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    location = models.JSONField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, default="active")

    def __str__(self):
        return f"{self.name}, {self.address}"

