from asgiref.sync import sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import *
from .serializers import *

class DriversLocationConsumer(AsyncWebsocketConsumer):
    """
    Hamma faol haydovchilar joylashuvlari
    """
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("driver_location_group", self.channel_name)
        await self.send_initial_driver_loc_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("driver_location_group", self.channel_name)

    async def send_initial_driver_loc_list(self):
        drivers_list = await self.get_locations_list()
        for driver in drivers_list:
            driver['id'] = str(driver['id'])
            driver['driver']['id'] = str(driver['driver']['id'])
            driver['driver']['warehouse']['id'] = str(driver['driver']['warehouse']['id'])
            driver['driver']['car']['driver'] = str(driver['driver']['car']['driver'])
        await self.send(text_data=json.dumps(drivers_list))

    async def add_new_driver_location(self, event):
        await self.send_initial_driver_loc_list()

    @sync_to_async
    def get_locations_list(self):
        loc_objects = DriverLocation.objects.filter(
            driver__is_available=True,
            driver__warehouse__isnull=False,
            driver__car__isnull=False
        ).order_by("-id")
        serializer = DriverLocationSerializer(loc_objects, many=True)
        return serializer.data

