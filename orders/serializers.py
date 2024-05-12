from rest_framework import serializers

from .models import *
from users.serializers import UserSerializer
from customers.serializers import CustomerStoreSerializer
from warehouses.serializers import WarehouseProductGetSerializer, WarehouseSerializer

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerStoreSerializer(read_only = True)
    product = WarehouseProductGetSerializer(read_only = True)
    warehouse = WarehouseSerializer(read_only = True)
    operator = UserSerializer(read_only = True)
    driver = UserSerializer(read_only = True)

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

