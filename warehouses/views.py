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

class WarehouseProductCreteOrUpdate(APIView):
    @swagger_auto_schema(request_body=WarehouseProductSerializer)
    def post(self, request):
        serializer = WarehouseProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        warehouse_product, created = WarehouseProduct.objects.get_or_create(
            warehouse=validated_data['warehouse'],
            product=validated_data['product'],
            defaults={'amount': validated_data['amount']}
        )
        if not created:
            warehouse_product.amount += validated_data['amount']
            warehouse_product.save()
        WarehouseProductArrival.objects.create(
            warehouse_product=warehouse_product,
            amount=validated_data['amount'],
            comment=validated_data['comment']
        )
        serializer = WarehouseProductSerializer(warehouse_product)
        return Response({"warehouse_product": serializer.data})

class WarehouseProductDetailAPIView(APIView):
    def get(self, request, ware_pk, pr_pk):
        ware_product = get_object_or_404(WarehouseProduct.objects.all(), id=pr_pk, warehouse__id=ware_pk)
        serializer = WarehouseProductSerializer(ware_product)
        return Response(serializer.data)

    def delete(self, request, ware_pk, pr_pk):
        warehouse_product = get_object_or_404(WarehouseProduct.objects.all(), id=pr_pk, warehouse__id=ware_pk)
        serializer = WarehouseProductSerializer(warehouse_product)
        warehouse_product.delete()
        return Response({"message": "deleted", "warehouse_product": serializer.data})

class WarehouseCustomersAPIView(APIView):
    def get(self, request, pk):
        warehouse_clients = CustomerStore.objects.filter(warehouse__id=pk)
        serializer = CustomerStoreSerializer(warehouse_clients, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CustomerStoreSerializer)
    def post(self, request, pk):
        warehouse = get_object_or_404(Warehouse.objects.all(), id=pk)
        serializer = CustomerStoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(warehouse=warehouse)
        return Response(serializer.data, status.HTTP_200_OK)

class WarehouseEmployeesAPIView(APIView):
    def get(self, request, pk):
        employees = CustomUser.objects.filter(
            warehouse__id = pk
        )
        role = request.query_params.get("role")
        if role:
            employees = employees.filter(role = role.lower())
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data)

class WarehouseTasksAPIView(APIView):
    def get(self, request, pk):
        warehouse_users = CustomUser.objects.filter(warehouse__id = pk)
        tasks = Task.objects.filter(task_executors__in = warehouse_users)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class WarehousesAPIView(APIView):
    def get(self, request):
        warehouses = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=WarehouseSerializer)
    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
