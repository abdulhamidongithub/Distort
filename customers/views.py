from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import CustomerStore
from .serializers import *

class CustomersAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="You can search by name, address, phone", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        customers = CustomerStore.objects.all()
        search = request.query_params.get("search")
        if search:
            customers = customers.filter(name__icontains=search
                        ) | customers.filter(address__icontains = search
                        ) | customers.filter(phone__icontains = search)
        serializer = CustomerStoreSerializer(customers, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CustomerStoreSerializer)
    def post(self, request):
        serializer = CustomerStoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(added_by = request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)

class CustomerDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        customer = get_object_or_404(CustomerStore.objects.all(), id=pk)
        serializer = CustomerStoreSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = get_object_or_404(CustomerStore.objects.all(), id=pk)
        serializer = CustomerStoreSerializer(customer)
        customer.delete()
        return Response({"message": "deleted", "customer": serializer.data})

    @swagger_auto_schema(request_body=CustomerStoreSerializer)
    def put(self, request, pk):
        customer = get_object_or_404(CustomerStore.objects.all(), id=pk)
        serializer = CustomerStoreSerializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


