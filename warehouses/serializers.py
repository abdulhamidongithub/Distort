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


