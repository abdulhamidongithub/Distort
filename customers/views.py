from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *

class CustomersAPIView(APIView):
    def get(self, request):
        customers = CustomerStore.objects.all()
        search = request.query_params.get("search")
        if search:
            customers = customers.filter(name__icontains=search
                        ) | customers.filter(address__icontains = search
                        ) | customers.filter(phone__icontains = search)
        serializer = CustomerStoreSerializer(customers, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
