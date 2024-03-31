from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import *
from customers.models import CustomerStore
from customers.serializers import CustomerStoreSerializer
from users.models import CustomUser, Task
from users.serializers import UserSerializer, TaskSerializer
from .serializers import *

class WarehouseProductsAPIView(APIView):
    def get(self, request, pk):
        ware_products = WarehouseProduct.objects.filter(warehouse__id=pk)
        serializer = WarehouseProductSerializer(ware_products, many=True)
        return Response(serializer.data)

class WarehouseCustomersAPIView(APIView):
    def get(self, request, pk):
        warehouse_clients = CustomerStore.objects.filter(warehouse__id=pk)
        serializer = CustomerStoreSerializer(warehouse_clients, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CustomerStoreSerializer)
    def post(self, request, pk):
        warehouse = get_object_or_404(Warehouse.objects.all(), id=pk)
        serializer = CustomerStoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(warehouse=warehouse)
        return Response(serializer.data, status.HTTP_200_OK)

class WarehouseAgentsAPIView(APIView):
    def get(self, request, pk):
        agents = CustomUser.objects.filter(
            warehouse__id = pk, role = 'Agent'
        )
        serializer = UserSerializer(agents, many=True)
        return Response(serializer.data)

class WarehouseTasksAPIView(APIView):
    def get(self, request, pk):
        warehouse_users = CustomUser.objects.filter(warehouse__id = pk)
        tasks = Task.objects.filter(task_executors__in = warehouse_users)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


