from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'phone_number', "role", "username", "address",
            "birth_date", "status", "warehouse"
            ]

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        car = Car.objects.filter(driver=instance)
        if car.exists():
            serializer = CarSerializer(car.first())
            data.update({"car": serializer.data})
        return data


class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = '__all__'

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

