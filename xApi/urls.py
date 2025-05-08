
from django.contrib import admin
from django.urls import path, include 
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi 
from rest_framework import permissions 
from django.conf import settings
from django.conf.urls.static import static 

schema_view = get_schema_view(
    openapi.Info(
        title="xApi",
        default_version='v0',
        description="API documentation for xApi",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dev@xapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


api_dcoumentaion_urls = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

API_URL = 'api/v0/'


urlpatterns = api_dcoumentaion_urls + [
    path(API_URL, include('xApiAuthentication.urls')),
]


urlpatterns += [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
