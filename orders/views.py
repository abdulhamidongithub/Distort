from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *
from warehouse.models import WarehouseProduct

class OrdersAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        date = request.query_params.get("date")
        status = request.query_params.get("status")
        if date:
            orders = orders.filter(date_time__startswith=date)
        if status:
            orders = orders.filter(status=status)
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
            },
            status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        order = request.data
        product = WarehouseProduct.objects.get(id=order.get("product"))
        if product.amount < order.amount:
            return Response({"success": "false", "message": f"Miqdor yetarli emas. Mavjud miqdor: {product.amount}"})
        serializer = OrderSerializer(data=order)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class OrderAPIView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.all(), id=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=OrderSerializer)
    def put(self, request, pk):
        saved_order = get_object_or_404(Order.objects.all(), id=pk)
        data = request.data
        serializer = OrderSerializer(instance=saved_order, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_order = serializer.save()
        return Response({"Order updated": saved_order})

class DriverOrdersAPIView(APIView):
    def get(self, request):
        driver = request.user
        orders = Order.objects.filter(driver=driver)
        date = request.query_params.get("date")
        status = request.query_params.get("status")
        if date:
            orders = orders.filter(date_time__startswith=date)
        if status:
            orders = orders.filter(status=status)
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
            },
            status.HTTP_200_OK
        )
