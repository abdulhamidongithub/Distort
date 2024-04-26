from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken

from .models import *
from .serializers import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UsersAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        role = request.query_params.get("role")
        if role:
            users = users.filter(role = role.lower())
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

class UserAPIView2(APIView):
    # User details based on the token
    def get(self, request, access_token):
        try:
            token = AccessToken(access_token)
            user_id = token.payload['user_id']
            user = CustomUser.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({"success": "false", "message": "User not found"}, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, access_token):
        try:
            token = AccessToken(access_token)
            user_id = token.payload['user_id']
            saved_user = CustomUser.objects.get(id=user_id)
            data = request.data
            serializer = UserSerializer(instance=saved_user, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                saved_user = serializer.save()
            return Response({"User updated": saved_user})
        except Exception as e:
            return Response({"success": "false", "message": "User not found"}, status.HTTP_400_BAD_REQUEST)


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
    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def put(self, request):
        serializer = ChangePasswordSerializer(instance=self.request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskCreateAPIView(APIView):
    @swagger_auto_schema(request_body=TaskSerializer)
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

