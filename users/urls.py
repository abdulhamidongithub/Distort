from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path('get_token/', MyTokenObtainPairView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
    path('change_password/', ChangePasswordAPIView.as_view()),

    path('salary_payments/', UserSalaryPaymentsAPIView.as_view()),
    path('details/<str:pk>/', UserAPIView.as_view()),
    path('details/token/<str:access_token>/', UserAPIView2.as_view()),
    path('all/', UsersAPIView.as_view()),
    path('car/<str:pk>/', CarUpdateAPIView.as_view()),
    path('car_create/', CarAddAPIView.as_view()),
    path('task_create/', TaskCreateAPIView.as_view()),
    path('olgan_tasklari/', UserReceivedTasks.as_view()),
    path('bergan_tasklari/', UserAssignedTasks.as_view()),
]

