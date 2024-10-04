from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from services import views

app_name = "services"

router = routers.SimpleRouter()
router.register(r'api/user', views.UserViewSet, basename='api-user')
router.register(r'api/workspace', views.WorkspaceViewSet, basename='api-workspace')

chat_urlpatterns = [
    path('', views.chat, name="api-chat"),
]

urlpatterns = router.urls + [
    path('api/token/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api-refresh'),
    path('api/chat/', include(chat_urlpatterns)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='services:schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='services:schema'), name='redoc'),
]