from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import *
from .serializers import *

class ProductsAPIView(APIView):
    def get(self, request):
        ware_products = WarehouseProduct.objects.all()
        serializer = WarehouseProductSerializer(ware_products, many=True)
        return Response(serializer.data)

