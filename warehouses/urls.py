from django.urls import path

from .views import *

urlpatterns = [
    path('<str:pk>/products/', WarehouseProductsAPIView.as_view()),
    path('<str:pk>/clients/', WarehouseClientsAPIView.as_view()),
]

