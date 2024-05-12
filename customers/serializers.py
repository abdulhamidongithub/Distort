from rest_framework import serializers

from .models import CustomerStore
from users.serializers import UserSerializer
from users.models import CustomUser
from warehouses.serializers import WarehouseSerializer
from warehouses.models import Warehouse

class CustomerStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerStore
        fields = '__all__'
        extra_kwargs = {
            'status': {'required': False},
            'created_at': {'required': False}
        }

    def to_representation(self, instance):
        data = super(CustomerStoreSerializer, self).to_representation(instance)
        if instance.warehouse:
            warehouse = WarehouseSerializer(Warehouse.objects.get(id=instance.warehouse.id))
            data.update({"warehouse": warehouse.data})
        if instance.added_by:
            user = UserSerializer(CustomUser.objects.get(id=instance.added_by.id))
            data.update({"added_by": user.data})
        return data