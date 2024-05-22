from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=30, blank=True, null=True, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", "-id"]

class Product(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    about = models.TextField(
        blank=True,
        null=True
    )
    photo = models.FileField(
        upload_to='products',
        null=True,
        blank=True
    )
    price = models.PositiveIntegerField()
    status = models.CharField(max_length=30, blank=True, null=True, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", "-id"]

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.start_date}-{self.end_date} {self.product.name} uchun {self.discount}% chegirma"


