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
from rest_framework.pagination import PageNumberPagination

from .models import *
from customers.models import CustomerStore
from products.models import Product
from customers.serializers import CustomerStoreSerializer
from users.models import CustomUser, Task
from orders.models import Order
from users.serializers import UserSerializer, TaskSerializer, TaskGetSerializer
from orders.serializers import OrderSerializer
from .serializers import *


class WarehouseProductsAPIView(APIView):
    def get(self, request, pk):
        warehouse = get_object_or_404(Warehouse.objects.all(), id=pk)
        ware_products = WarehouseProduct.objects.filter(warehouse = warehouse)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(ware_products, request)
        serializer = WarehouseProductGetSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class WarehouseProductCreate(APIView):
    @swagger_auto_schema(request_body=WarehouseProductSerializer)
    def post(self, request):
        serializer = WarehouseProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        warehouse = get_object_or_404(Warehouse.objects.all(), id=validated_data['warehouse'])
        product = get_object_or_404(Product.objects.all(), id=validated_data['product'])
        warehouse_product = WarehouseProduct.objects.create(
            warehouse=warehouse,
            product=product,
            amount = validated_data.get('amount'),
            invalids_amount = validated_data.get(('invalids_amount'), 0)
        )
        # WarehouseProductArrival.objects.create(
        #     warehouse_product=warehouse_product,
        #     amount=validated_data['amount'],
        #     comment=validated_data.get("comment", None)
        # )
        serializer = WarehouseProductSerializer(warehouse_product)
        return Response({"warehouse_product": serializer.data})

class WarehouseProductDetailAPIView(APIView):
    def get(self, request, ware_pk, pr_pk):
        ware_product = get_object_or_404(WarehouseProduct.objects.all(), id=pr_pk, warehouse__id=ware_pk)
        serializer = WarehouseProductGetSerializer(ware_product)
        return Response(serializer.data)

    def delete(self, request, ware_pk, pr_pk):
        warehouse_product = get_object_or_404(WarehouseProduct.objects.all(), id=pr_pk, warehouse__id=ware_pk)
        warehouse_product.delete()
        return Response({"success" :"true", "message": "deleted"})

    @swagger_auto_schema(request_body=WarehouseProductSerializer)
    def put(self, request, ware_pk, pr_pk):
        warehouse_product = get_object_or_404(WarehouseProduct.objects.all(), id=pr_pk)
        serializer = WarehouseProductSerializer(instance=request.data, data=warehouse_product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class WarehouseCustomersAPIView(APIView):
    def get(self, request, pk):
        warehouse_clients = CustomerStore.objects.filter(warehouse__id=pk)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(warehouse_clients, request)
        serializer = CustomerStoreSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

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
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(employees, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class WarehouseTasksAPIView(APIView):
    def get(self, request, pk):
        warehouse_users = CustomUser.objects.filter(warehouse__id = pk)
        tasks = Task.objects.filter(task_executors__in = warehouse_users)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskGetSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class WarehousesAPIView(APIView):
    def get(self, request):
        warehouses = Warehouse.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(warehouses, request)
        serializer = WarehouseSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

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
            "tasks": TaskGetSerializer(tasks, many=True).data
        }
        return Response(context, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=WarehouseSerializer)
    def put(self, request, pk):
        warehouse = get_object_or_404(Warehouse.objects.all(), id=pk)
        serializer = WarehouseSerializer(warehouse, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        warehouse = get_object_or_404(Warehouse.objects.all(), id=pk)
        warehouse.delete()
        return Response({"message": "deleted", "message": "Warehouse deleted"})

class WarehouseOrdersAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('date', openapi.IN_QUERY, description="Filter by date", type=openapi.TYPE_STRING),
        openapi.Parameter('status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING),
        openapi.Parameter('customer', openapi.IN_QUERY, description="Filter by customer ID, name, address, or phone",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('product', openapi.IN_QUERY, description="Filter by product ID or name",
                          type=openapi.TYPE_STRING),
    ])
    def get(self, request, pk):
        orders = Order.objects.filter(warehouse__id = pk)
        date = request.query_params.get("date")
        order_status = request.query_params.get("status")
        customer = request.query_params.get("customer")
        product = request.query_params.get("product")
        if order_status:
            order_status = order_status.split("-")
            orders = orders.filter(status=order_status[0])
            for status in order_status[1:]:
                orders = orders | Order.objects.filter(status=status, warehouse__id = pk)
        if customer:
            orders = orders.filter(customer__id=customer
                    ) | orders.filter(customer__name__icontains=customer
                    ) | orders.filter(customer__address__icontains=customer
                    ) | orders.filter(customer__phone__icontains=customer)
        if product:
            orders = orders.filter(product__id=product
                                   ) | orders.filter(product__name__icontains=product)
        if date:
            orders = orders.filter(date_time__startswith=date)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
