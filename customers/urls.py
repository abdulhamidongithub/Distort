from django.urls import path

from .views import *

urlpatterns = [
    path('all/', CustomersAPIView.as_view()),
]

