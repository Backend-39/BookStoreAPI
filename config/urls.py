from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_refresh
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf.urls.static import static
from django.conf import settings


schema_view = get_schema_view(
   openapi.Info(
      title="BookStore Api",
      default_version='v1',
      description="BookStore loyihasi uchun api.",
      terms_of_service="t.me://shuhratrozimatov",
      contact=openapi.Contact(email="shuhratrozimatov06@gmail.com"),
      license=openapi.License(name="Hozircha yo'q."),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/token/obtain/', token_obtain_pair),
    path('api/token/refresh/', token_refresh),
    path('api/', include('api.urls')),
    
]

urlpatterns += static(
    settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
)
