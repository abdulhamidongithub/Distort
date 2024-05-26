from rest_framework import serializers

from .models import *
from users.serializers import UserSerializer
from customers.serializers import CustomerStoreSerializer
from warehouses.serializers import WarehouseProductGetSerializer, WarehouseSerializer
from warehouses.models import Warehouse, WarehouseProduct

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'warehouse_product', 'amount', 'tot_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'deadline': {'required': False},
            'comment': {'required': False},
            'status': {'required': False},
            'date_time': {'required': False},
            'discount': {'required': False},
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        order.save()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.customer = validated_data.get('customer', instance.customer)
        instance.operator = validated_data.get('operator', instance.operator)
        instance.warehouse = validated_data.get('warehouse', instance.warehouse)
        instance.driver = validated_data.get('driver', instance.driver)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        for item_data in items_data:
            warehouse_product = item_data.get('warehouse_product')
            amount = item_data.get('amount')

            item, created = OrderItem.objects.update_or_create(
                order=instance,
                warehouse_product=warehouse_product
            )
            if created:
                created.amount = amount
                created.save()
            else:
                item.amount = amount
                item.save()

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        data['items'] = OrderItemSerializer(instance.items.all(), many=True).data
        if instance.warehouse:
            warehouse = WarehouseSerializer(instance.warehouse)
            data.update({"warehouse": warehouse.data})
        if instance.operator:
            user = UserSerializer(instance.operator)
            data.update({"operator": user.data})
        if instance.driver:
            user = UserSerializer(instance.driver)
            data.update({"driver": user.data})
        if instance.customer:
            customer = CustomerStoreSerializer(instance.customer)
            data.update({"customer": customer.data})
        return data


