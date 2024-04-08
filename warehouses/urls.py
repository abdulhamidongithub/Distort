from django.urls import path

from .views import *

urlpatterns = [
    path('<str:pk>/products/', WarehouseProductsAPIView.as_view()),
    path('<str:ware_pk>/products/<str:pr_pk>/', WarehouseProductDetailAPIView.as_view()),
    path('<str:pk>/customers/', WarehouseCustomersAPIView.as_view()),
    path('<str:pk>/employees/', WarehouseEmployeesAPIView.as_view()),
    path('<str:pk>/tasks/', WarehouseTasksAPIView.as_view()),
    path('all/', WarehousesAPIView.as_view()),
    path('warehouse_product/create/', WarehouseProductCreteOrUpdate.as_view()),
]
