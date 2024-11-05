from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from services import views
from workspace.api.v1.views import StudioViewSet
from account.api.v1.views import UserViewSet, CustomTokenViewBase

app_name = "services"

router = routers.SimpleRouter()
router.register(r'v1/user', UserViewSet, basename='api-user')
router.register(r'workspace', views.WorkspaceViewSet, basename='api-workspace')
router.register(r'v1/studio', StudioViewSet, basename='api-studio')

chat_urlpatterns = [
    path('', views.chat, name="api-chat"),
]

urlpatterns = router.urls + [
    path('token/', CustomTokenViewBase.as_view(), name='api-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api-refresh'),
    path('chat/', include(chat_urlpatterns)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='services:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='services:schema'), name='redoc'),
]