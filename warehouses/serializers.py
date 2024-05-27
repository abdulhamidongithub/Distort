from rest_framework import serializers

from .models import *
from products.serializers import ProductSerializer
from products.models import Product

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class WarehouseProductSerializer(serializers.Serializer):
    product = serializers.UUIDField(required=False)
    warehouse = serializers.UUIDField(required=False)
    amount = serializers.IntegerField(required=False)
    total_sum = serializers.IntegerField(required=False)
    invalids_amount = serializers.IntegerField(required=False)
    archived = serializers.BooleanField(required=False)
    comment = serializers.CharField(required=False)

class WarehouseProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = ['id', 'product', 'warehouse', 'amount', 'invalids_amount', "total_sum"]

    def to_representation(self, instance):
        data = super(WarehouseProductGetSerializer, self).to_representation(instance)
        if instance.warehouse:
            warehouse = WarehouseSerializer(Warehouse.objects.get(id=instance.warehouse.id))
            data.update({"warehouse": warehouse.data})
        if instance.product:
            product = ProductSerializer(Product.objects.get(id=instance.product.id))
            data.update({"product": product.data})
        return data

class WarehouseProductArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProductArrival
        fields = ["id", "warehouse_product", "amount", "invalids_amount", "comment", "date_time"]
        extra_kwargs = {
            'comment': {'required': False},
            'date_time': {'required': False},
            'invalids_amount': {'required': False},
            'amount': {'required': False}
        }

    def create(self, validated_data):
        warehouse_product_arrival = super().create(validated_data)

        warehouse_product = warehouse_product_arrival.warehouse_product
        warehouse_product.amount += validated_data.get('amount', 0)
        warehouse_product.invalids_amount += validated_data.get('invalids_amount', 0)
        warehouse_product.amount -= validated_data.get('invalids_amount', 0)
        warehouse_product.save()

        return warehouse_product_arrival

