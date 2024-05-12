from rest_framework import serializers

from .models import *
from products.serializers import ProductSerializer

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class WarehouseProductSerializer(serializers.Serializer):
    product = serializers.UUIDField()
    warehouse = serializers.UUIDField()
    amount = serializers.IntegerField()
    invalids_amount = serializers.IntegerField(required=False)
    comment = serializers.CharField(required=False)

class WarehouseProductGetSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = WarehouseProduct
        fields = ['id', 'product', 'warehouse', 'amount', 'invalids_amount']
