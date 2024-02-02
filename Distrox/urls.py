from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Distrox API",
      default_version='v1',
      description="web-API's for a distribution firm",
      contact=openapi.Contact(email="1997abdulhamid@gmail.com"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger_docs/', schema_view.with_ui('swagger', cache_timeout=0)),
]
