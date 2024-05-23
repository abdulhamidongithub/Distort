from django.urls import path

from .views import *

urlpatterns = [
    path('all/', OrdersAPIView.as_view()),
    path('<int:pk>/details/', OrderAPIView.as_view()),
    path('driver_orders/<str:driver_id>/', DriverOrdersAPIView.as_view()),
    path('customer_orders/<str:customer_id>/', CustomerOrdersAPIView.as_view()),
    path('operator_orders/<str:operator_id>/', OperatorOrdersAPIView.as_view()),
]
