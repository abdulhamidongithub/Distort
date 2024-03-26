from django.urls import path

from .views import *

urlpatterns = [
    path('products/', WarehouseProductsAPIView.as_view()),
]

