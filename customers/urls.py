from django.urls import path

from .views import *

urlpatterns = [
    path('all/', CustomersAPIView.as_view()),
    path('<str:pk>/detail/', CustomerDetailView.as_view()),
]

