from rest_framework import routers
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from services import views

app_name = "services"

router = routers.SimpleRouter()
router.register(r'api/workspace', views.WorkspaceViewSet, basename='workspace')

chat_urlpatterns = [
    path('', views.chat, name="chat"),
]

urlpatterns = router.urls + [
    path('api/chat/', include(chat_urlpatterns)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='services:schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='services:schema'), name='redoc'),
]