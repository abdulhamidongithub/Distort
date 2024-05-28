from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from warehouses.serializers import WarehouseSerializer

from .models import *

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    driver_device_token = serializers.CharField(required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        driver_device_token = attrs.get('driver_device_token', None)

        user = CustomUser.objects.filter(username=username, password=password).first()
        if user is None:
            raise serializers.ValidationError({
                'success': "false",
                'message': 'User not found'
            }, code=status.HTTP_400_BAD_REQUEST)
        if user.archived:
            raise serializers.ValidationError({
                'success': "false",
                'message': 'User arxivlangan'
            }, code=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        warehouse = None
        if user.warehouse:
            warehouse = WarehouseSerializer(user.warehouse).data
        if driver_device_token:
            user.driver_device_token = driver_device_token
            user.save()
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            "id": user.id,
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
            "archived": user.archived
        }

class UserSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'id', "first_name", "last_name", 'phone_number', "role", "username", "password", "address",
            "birth_date", "status", "warehouse", "is_available", "photo", "archived"
            ]

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        car = Car.objects.filter(driver=instance)
        if car.exists():
            serializer = CarSerializer(car.first())
            data.update({"car": serializer.data})
        return data

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', "first_name", "last_name", 'phone_number', "role", "username", "password", "address",
            "birth_date", "status", "warehouse", "is_available", "photo"
            ]

class SalaryParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryParams
        fields = '__all__'

    def to_representation(self, instance):
        data = super(SalaryParamsSerializer, self).to_representation(instance)
        if instance.user:
            user = UserSerializer(CustomUser.objects.get(id=instance.user.id))
            data.update({"user": user.data})
        return data

class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = '__all__'
        extra_kwargs = {
            'paid_at': {'required': False},
            'payer': {'required': False}
        }

    def to_representation(self, instance):
        data = super(SalaryPaymentSerializer, self).to_representation(instance)
        if instance.user:
            user = UserSerializer(CustomUser.objects.get(id=instance.user.id))
            data.update({"user": user.data})
        if instance.payer:
            user = UserSerializer(CustomUser.objects.get(id=instance.payer.id))
            data.update({"payer": user.data})
        return data

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    def validate_driver(self, driver):
        car = Car.objects.filter(driver__id = driver)
        if car.exists():
            raise APIException("Haydovchida allaqachon biriktirilgan mashina bor")
        return driver


class TaskSerializer(serializers.ModelSerializer):
    task_executors = serializers.PrimaryKeyRelatedField(
    many=True,
    queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Task
        fields = '__all__'

class TaskGetSerializer(serializers.ModelSerializer):
    task_executors = UserSerializer(many = True, read_only=True)
    task_setter = UserSerializer(read_only=True)

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

class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLocation
        fields = '__all__'
        extra_kwargs = {
            'driver': {'read_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        driver = data.get('driver')
        driver = CustomUser.objects.filter(id=driver).first()
        driver_ser = UserSerializer(driver)
        data['driver'] = driver_ser.data
        return data


