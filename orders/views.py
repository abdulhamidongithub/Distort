from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

class OrdersAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        order = request.data
        serializer = OrderSerializer(data=order)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class OrderAPIView(APIView):
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


    def put(self, request, pk):
        saved_order = get_object_or_404(Order.objects.all(), pk=pk)
        data = request.data
        serializer = OrderSerializer(instance=saved_order, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_order = serializer.save()
        return Response({"Order updated": saved_order})
