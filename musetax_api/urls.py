from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from musetax_api import settings
from tenants.api.views import RefreshTokenView, TokenView

schema_view = get_schema_view(
   openapi.Info(
      title='Muse API',
      default_version='v1',
      description='MuseTax API endpoints',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='admin@musetax.com'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('token/', TokenView.as_view(), name='token'),
    path('token/refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('api/', include('tenants.api.urls')),
    path('api/', include('users.api.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
