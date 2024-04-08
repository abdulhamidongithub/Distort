from rest_framework import serializers

from .models import *

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class WarehouseProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    product = serializers.IntegerField()
    warehouse = serializers.IntegerField()
    amount = serializers.IntegerField()
    invalids_amount = serializers.IntegerField()
    comment = serializers.CharField()


    def create(self, validated_data):
        warehouse_product, created = WarehouseProduct.objects.get_or_create(
            warehouse=validated_data['warehouse'],
            product=validated_data['product'],
            defaults={'amount': validated_data['amount']}
        )
        if not created:
            warehouse_product.amount += validated_data['amount']
            warehouse_product.save()
        WarehouseProductArrival.objects.create(
            warehouse_product = warehouse_product,
            amount = validated_data['amount'],
            comment = validated_data['comment']
        )
        return warehouse_product

