from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from django.urls import path

from .views import *

urlpatterns = [
    path('get_token/', TokenObtainPairView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
    path('change_password/', ChangePasswordAPIView.as_view()),

    path('salary_payments/', UserSalaryPaymentsAPIView.as_view()),
    path('details/<str:pk>/', UserAPIView.as_view()),
    path('car/<str:pk>/', CarUpdateAPIView.as_view()),
]

