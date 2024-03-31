from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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
