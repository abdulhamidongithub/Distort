from rest_framework import serializers

from .models import CustomerStore

class CustomerStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerStore
        fields = '__all__'
