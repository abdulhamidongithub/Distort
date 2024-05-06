from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from warehouses.serializers import WarehouseSerializer

from .models import *

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = CustomUser.objects.filter(username=username, password=password).first()
        if user is None:
            raise serializers.ValidationError({
                'success': "false",
                'message': 'User not found'
            }, code=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        if user.warehouse:
            warehouse = WarehouseSerializer(user.warehouse).data
        else:
            warehouse = None
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            "username": username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone_number,
            "role": user.role,
            "address": user.address,
            "birth_date": user.birth_date,
            "warehouse": warehouse,
            "status": user.status,
            "is_available": user.is_available,
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', "first_name", "last_name", 'phone_number', "role", "username", "password", "address",
            "birth_date", "status", "warehouse", "is_available"
            ]

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        car = Car.objects.filter(driver=instance)
        if car.exists():
            serializer = CarSerializer(car.first())
            data.update({"car": serializer.data})
        return data

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.role = validated_data.get('role', instance.role)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.warehouse = validated_data.get('warehouse', instance.warehouse)
        instance.address = validated_data.get('address', instance.address)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.status = validated_data.get('status', instance.status)
        instance.is_available = validated_data.get('is_available', instance.is_available)

        instance.save()
        return instance


class SalaryParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryParams
        fields = '__all__'

class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = '__all__'
        extra_kwargs = {
            'paid_at': {'required': False},
            'payer': {'required': False}
        }

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.number = validated_data.get('number', instance.number)
        instance.driver = validated_data.get('driver', instance.driver)

        instance.save()
        return instance

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    re_new_password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):

        instance.password = validated_data.get('password', instance.password)
        if not validated_data['new_password']:
              raise serializers.ValidationError({'new_password': 'not found'})

        if not validated_data['old_password']:
              raise serializers.ValidationError({'old_password': 'not found'})

        if instance.password != validated_data['old_password']:
              raise serializers.ValidationError({'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['re_new_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['re_new_password'] and instance.password == validated_data['old_password']:
            instance.password = validated_data['new_password']
            instance.save()
            return instance

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password','re_new_password']
