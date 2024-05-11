from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import *
from .serializers import *
from warehouses.models import WarehouseProduct
from users.models import CustomUser

class OrdersAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('date', openapi.IN_QUERY, description="Filter by date", type=openapi.TYPE_STRING),
        openapi.Parameter('status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING),
        openapi.Parameter('customer', openapi.IN_QUERY, description="Filter by customer ID, name, address, or phone",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('product', openapi.IN_QUERY, description="Filter by product ID or name",
                          type=openapi.TYPE_STRING),
    ])
    def get(self, request):
        orders = Order.objects.all()
        date = request.query_params.get("date")
        order_status = request.query_params.get("status")
        customer = request.query_params.get("customer")
        product = request.query_params.get("product")
        if order_status:
            order_status = order_status.split("-")
            orders = orders.filter(status = order_status[0])
            for status in order_status[1:]:
                orders = orders | Order.objects.filter(status=status)
        if customer:
            orders = orders.filter( customer__id = customer
                ) | orders.filter( customer__name__icontains = customer
                ) | orders.filter( customer__address__icontains = customer
                ) | orders.filter(customer__phone__icontains = customer)
        if product:
            orders = orders.filter( product__id = product
                ) | orders.filter( product__name__icontains = product)
        if date:
            orders = orders.filter(date_time__startswith=date)
        counts = {
            "active": orders.filter(status="Active").count(),
            "delivered": orders.filter(status="Delivered").count(),
            "cancelled": orders.filter(status="Cancelled").count()
        }
        serializer = OrderSerializer(orders, many=True)
        return Response(
            {
                "counts": counts,
                "orders": serializer.data,
            }
        )

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        order = request.data
        product = WarehouseProduct.objects.get(id=order.get("product"))
        if product.amount < order.amount:
            return Response({"success": "false", "message": f"Miqdor yetarli emas. Mavjud miqdor: {product.amount}"})
        serializer = OrderSerializer(data=order)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class OrderAPIView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.all(), id=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, pk):
        order = get_object_or_404(Order.objects.all(), id=pk)
        serializer = OrderSerializer(order)
        order.delete()
        return Response({"message": "deleted", "order": serializer.data})

    @swagger_auto_schema(request_body=OrderSerializer)
    def put(self, request, pk):
        saved_order = get_object_or_404(Order.objects.all(), id=pk)
        data = request.data
        serializer = OrderSerializer(instance=saved_order, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        saved_order = serializer.save()
        saved_order = OrderSerializer(saved_order).data
        return Response(saved_order)

class DriverOrdersAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('date', openapi.IN_QUERY, description="Filter by date", type=openapi.TYPE_STRING),
        openapi.Parameter('status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING)
    ])
    def get(self, request, driver_id):
        driver = get_object_or_404(CustomUser.objects.all(), id=driver_id)
        if not driver.is_available:
            return Response({"success":"false", "message": "Driver is not available"})
        orders = Order.objects.filter(driver=driver)
        date = request.query_params.get("date")
        order_status = request.query_params.get("status")
        if order_status:
            order_status = order_status.split("-")
            orders = orders.filter(status = order_status[0])
            for status in order_status[1:]:
                orders = orders | Order.objects.filter(status=status)
        if date:
            orders = orders.filter(date_time__startswith=date)
        counts = {
            "active": orders.filter(status="Active").count(),
            "delivered": orders.filter(status="Delivered").count(),
            "cancelled": orders.filter(status="Cancelled").count()
        }
        serializer = OrderSerializer(orders, many=True)
        return Response(
            {
                "counts": counts,
                "orders": serializer.data,
            }
        )
