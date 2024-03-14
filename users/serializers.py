from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'phone_number', "role", "username", "address",
            "birth_date", "status", "warehouse"
            ]
