from rest_framework import serializers

from .models import *
from users.serializers import UserSerializer
from customers.serializers import CustomerStoreSerializer
from warehouses.serializers import WarehouseProductGetSerializer, WarehouseSerializer
from warehouses.models import Warehouse, WarehouseProduct


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'deadline': {'required': False},
            'comment': {'required': False},
            'status': {'required': False},
            'customer': {'required': False},
            'date_time': {'required': False},
            'discount': {'required': False},
        }

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        if instance.warehouse:
            warehouse = WarehouseSerializer(Warehouse.objects.get(id=instance.warehouse.id))
            data.update({"warehouse": warehouse.data})
        if instance.warehouse_product:
            ware_product = WarehouseProductGetSerializer(WarehouseProduct.objects.get(id=instance.warehouse_product.id))
            data.update({"product": ware_product.data})
        if instance.operator:
            user = UserSerializer(CustomUser.objects.get(id=instance.operator.id))
            data.update({"operator": user.data})
        if instance.driver:
            user = UserSerializer(CustomUser.objects.get(id=instance.driver.id))
            data.update({"driver": user.data})
        if instance.customer:
            customer = CustomerStoreSerializer(CustomerStore.objects.get(id=instance.customer.id))
            data.update({"customer": customer.data})
        return data

