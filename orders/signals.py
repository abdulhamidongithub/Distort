from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from .models import Order, KPIEarning
from users.models import SalaryParams


@receiver(post_save, sender=Order)
def decrement_amount_on_order_create(sender, instance, created, **kwargs):
    if created:
        warehouse_product = instance.warehouse_product
        warehouse_product.amount -= instance.amount
        warehouse_product.save()


@receiver(pre_save, sender=Order)
def create_kpi_earnings(sender, instance, **kwargs):
    if instance.status == 'Confirmed':
        original_order = Order.objects.get(pk=instance.pk)

        if original_order.status != "Confirmed":
            users = {
                'supervisor': instance.warehouse.customuser_set.filter(role='supervisor').last(),
                'branch_director': instance.warehouse.customuser_set.filter(role='branch_director').last(),
                'agent': instance.customer.added_by,
            }
            salary_params = {}
            for role, user in users.items():
                try:
                    salary_params[role] = SalaryParams.objects.get(user=user)
                except ObjectDoesNotExist:
                    salary_params[role] = None

            for role, user in users.items():
                if user and salary_params[role]:
                    amount = round(instance.total_price * (salary_params[role].kpi_by_sales / 100), 2)
                    KPIEarning.objects.create(
                        user=user,
                        order=instance,
                        amount=amount
                    )


@receiver(pre_save, sender=Order)
def return_amount_on_order_cancel(sender, instance, **kwargs):
    if instance.status == "Cancelled":
        try:
            original_order = Order.objects.get(pk=instance.pk)
            if original_order.status != "Cancelled":
                warehouse_product = instance.warehouse_product
                warehouse_product.amount += instance.amount
                warehouse_product.save()
        except Order.DoesNotExist:
            pass
