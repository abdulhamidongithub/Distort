from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination

from .models import *
from warehouses.models import WarehouseProduct
from .serializers import *

class ProductsAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search by name, about", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        products = Product.objects.all()
        search_word = request.query_params.get("search")
        if search_word:
            products = products.filter(name__icontains=search_word
                        ) | products.filter(about__icontains=search_word)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CategoriesAPIView(APIView):
    def get(self, request):
        categories = (Category.objects.all())
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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

    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.all(), id=pk)
        warehouse_products = WarehouseProduct.objects.filter(product = product)
        if warehouse_products.exists():
            return Response({"success": "false",
                            "message": "Bu mahsulot filiallarda mavjud. Avval filiallardan o'chirish kerak!"},
                            status.HTTP_406_NOT_ACCEPTABLE)
        product.delete()
        return Response({"success": "true", "message": "Product deleted"}, status.HTTP_200_OK)

class CategoryDetailAPIView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category.objects.all(), id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):
        category = get_object_or_404(Category.objects.all(), id=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.all(), id=pk)
        category.delete()
        return Response({"success": "true", "message": "Category deleted"}, status.HTTP_200_OK)
