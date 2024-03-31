from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *

class UsersAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class UserAPIView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser.objects.all(), id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserSalaryPaymentsAPIView(APIView):
    def get(self, request):
        user = request.user
        salary_payments = SalaryPayment.objects.filter(user=user)
        serializer = SalaryPaymentSerializer(salary_payments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class CarUpdateAPIView(APIView):
    @swagger_auto_schema(request_body=CarSerializer)
    def put(self, request, pk):
        car = get_object_or_404(Car.objects.all(), id=pk)
        serializer = CarSerializer(instance=car, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            car = serializer.save()
        return Response({"Car updated": car})

class ChangePasswordAPIView(APIView):
    def put(self, request):
        serializer = ChangePasswordSerializer(instance=self.request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskCreateAPIView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

