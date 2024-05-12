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
        }

class UserSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
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

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', "first_name", "last_name", 'phone_number', "role", "username", "password", "address",
            "birth_date", "status", "warehouse", "is_available"
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
        data = super(SalaryParamsSerializer, self).to_representation(instance)
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
