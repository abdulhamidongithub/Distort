from rest_framework import serializers

from .models import CustomerStore
from users.serializers import UserSerializer
from warehouses.serializers import WarehouseSerializer

class CustomerStoreSerializer(serializers.ModelSerializer):
    added_by = UserSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

    class Meta:
        model = CustomerStore
        fields = '__all__'
        extra_kwargs = {
            'status': {'required': False},
            'created_at': {'required': False}
        }
