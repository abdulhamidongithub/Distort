from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *

class ProductsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CategoriesAPIView(APIView):
    def get(self, request):
        categories = (Category.objects.all())
        serializer = ProductSerializer(categories, many=True)
        return Response(serializer.data)

class CategoryProductsAPIView(APIView):
    def get(self, request,pk):
        products = Product.objects.filter(category__id=pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product.objects.all(), id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):
        product = get_object_or_404(Product.objects.all(), id=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
