from rest_framework import serializers

from .models import CustomerStore
from users.serializers import UserSerializer  # Import UserSerializer from your users app

class CustomerStoreSerializer(serializers.ModelSerializer):
    added_by = UserSerializer(read_only=True)  # Nested serializer for added_by field

    class Meta:
        model = CustomerStore
        fields = '__all__'
        extra_kwargs = {
            'status': {'required': False},
            'created_at': {'required': False}
        }
