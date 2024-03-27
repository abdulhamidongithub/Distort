from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import *
from customers.models import CustomerStore
from customers.serializers import CustomerStoreSerializer
from users.models import CustomUser
from .serializers import *

class WarehouseProductsAPIView(APIView):
    def get(self, request, pk):
        ware_products = WarehouseProduct.objects.filter(warehouse__id=pk)
        serializer = WarehouseProductSerializer(ware_products, many=True)
        return Response(serializer.data)

class WarehouseClientsAPIView(APIView):
    def get(self, request, pk):
        ware_users = CustomUser.objects.filter(warehouse__id=pk)
        ware_clients = CustomerStore.objects.filter(agent__in=ware_users)
        serializer = CustomerStoreSerializer(ware_clients, many=True)
        return Response(serializer.data)