from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path('drivers_locations/', consumers.DriversLocationConsumer.as_asgi()),
]
