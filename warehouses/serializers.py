from rest_framework import serializers

from .models import *

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class WarehouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = '__all__'
        read_only_fields = ["invalids_amount", "date_time"]

    def create(self, validated_data):
        warehouse_product, created = WarehouseProduct.objects.get_or_create(
            warehouse=validated_data['warehouse'],
            product=validated_data['product'],
            defaults={'amount': validated_data['amount']}
        )
        if not created:
            warehouse_product.amount += validated_data['amount']
            warehouse_product.save()
        return warehouse_product

