from django.urls import path

from .views import *

urlpatterns = [
    path('all/', OrdersAPIView.as_view()),
    path('<int:pk>/details/', OrderAPIView.as_view()),
    path('driver_orders/<str:driver_id>/', DriverOrdersAPIView.as_view()),
]

