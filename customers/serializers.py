from rest_framework import serializers

from .models import CustomerStore

class CustomerStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerStore
        fields = '__all__'
        extra_kwargs = {
            'added_by': {'required': False},
            'status': {'required': False},
            'created_at': {'required': False}
        }

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.location = validated_data.get('location', instance.location)
        instance.status = validated_data.get('status', instance.status)
        instance.warehouse = validated_data.get('warehouse', instance.warehouse)

        instance.save()
        return instance
