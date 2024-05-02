from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from warehouses.models import Warehouse

ROLES = [
    ("admin", "admin"),
    ("manager", "manager"),
    ("branch_director", "branch_director"),
    ("supervisor", "supervisor"),
    ("operator", "operator"),
    ("agent", "agent"),
    ("driver", "driver")
]

class CustomUser(AbstractUser):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    phone_number = models.CharField(max_length=15)
    phone_number2 = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    address = models.CharField(max_length=100)
    birth_date = models.DateField(
        null=True,
        blank=True
    )
    photo = models.FileField(null=True, blank=True, upload_to="profile_photos")
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=30, default="active")
    role = models.CharField(
        max_length=30,
        choices=ROLES
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    balance = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class SalaryParams(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    fixed = models.PositiveIntegerField()
    kpi_by_sales = models.FloatField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


class SalaryPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="user_salary_payments")
    payer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="payer_payments")
    amount = models.FloatField()
    paid_at = models.DateTimeField()
    comment = models.TextField(null=True, blank=True)

class Car(models.Model):
    type = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

class Task(models.Model):
    text = models.TextField()
    task_setter = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null = True)
    task_executors = models.ManyToManyField('users.CustomUser', related_name='bajaruvchilar_tasklari')
    created_at = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30)
    def __str__(self):
        return self.text
