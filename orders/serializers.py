from rest_framework import serializers

from .models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.operator = validated_data.get('operator', instance.operator)
        instance.warehouse = validated_data.get('warehouse', instance.warehouse)
        instance.driver = validated_data.get('driver', instance.driver)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.date_time = validated_data.get('date_time', instance.date_time)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance
