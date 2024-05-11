from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from customers.models import CustomerStore
from products.models import Product
from customers.serializers import CustomerStoreSerializer
from users.models import CustomUser, Task
from orders.models import Order
from users.serializers import UserSerializer, TaskSerializer
from orders.serializers import OrderSerializer
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
        warehouse = get_object_or_404(Warehouse.objects.all(), id=validated_data['warehouse'])
        product = get_object_or_404(Product.objects.all(), id=validated_data['product'])
        warehouse_product, created = WarehouseProduct.objects.get_or_create(
            warehouse=warehouse,
            product=product,
            defaults={'amount': validated_data['amount']}
        )
        if not created:
            warehouse_product.amount += validated_data['amount']
            warehouse_product.save()
        WarehouseProductArrival.objects.create(
            warehouse_product=warehouse_product,
            amount=validated_data['amount'],
            comment=validated_data.get("comment", None)
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
        warehouse_product.delete()
        return Response({"success" :"true", "message": "deleted"})

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
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('role', openapi.IN_QUERY, description="Search by role", type=openapi.TYPE_STRING)
    ])
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

class WarehouseDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        warehouse = get_object_or_404(Warehouse.objects.all(), id=pk)
        today = timezone.now()
        four_weeks_ago = today - timedelta(weeks=4)
        orders = Order.objects.filter(
            date_time__gte=four_weeks_ago,
            warehouse = warehouse
        ).order_by('-date_time')

        warehouse_products = WarehouseProduct.objects.filter(warehouse=warehouse)
        tasks = Task.objects.filter(
            created_at__gte=four_weeks_ago,
            task_executors__warehouse = warehouse
        )
        customers = CustomerStore.objects.filter(warehouse=warehouse)
        users = CustomUser.objects.filter(warehouse=warehouse)
        counts = {
            "orders": orders.count(),
            "tasks": tasks.count(),
            "warehouse_products": warehouse_products.count(),
            "customers": customers.count(),
            "users": users.count()
        }
        context = {
            "counts": counts,
            "warehouse": WarehouseSerializer(warehouse).data,
            "orders": OrderSerializer(orders, many=True).data,
            "users": UserSerializer(users, many=True).data,
            "warehouse_products": WarehouseProductGetSerializer(warehouse_products, many=True).data,
            "customers": CustomerStoreSerializer(customers, many=True).data,
            "tasks": TaskSerializer(tasks, many=True).data
        }
        return Response(context, status.HTTP_200_OK)

    def delete(self, request, pk):
        warehouse = get_object_or_404(Warehouse.objects.all(), id=pk)
        warehouse.delete()
        return Response({"message": "deleted", "message": "Warehouse deleted"})


