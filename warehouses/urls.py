from django.urls import path

from .views import *

urlpatterns = [
    path('<str:pk>/products/', WarehouseProductsAPIView.as_view()),
    path('<str:pk>/customers/', WarehouseCustomersAPIView.as_view()),
    path('<str:pk>/agents/', WarehouseAgentsAPIView.as_view()),
    path('<str:pk>/tasks/', WarehouseAgentsAPIView.as_view()),
]
