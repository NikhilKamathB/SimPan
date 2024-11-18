from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from services import views
from workspace.api.v1.views import StudioViewSet
from account.api.v1.views import UserViewSet, CustomTokenViewBase

app_name = "services"

# V1 router and patterns
v1_router = routers.SimpleRouter()
v1_router.register(r'user', UserViewSet, basename='api-user')
v1_router.register(r'studio', StudioViewSet, basename='api-studio')
v1_patterns = [
    # Router URLs
    path('', include((v1_router.urls, 'v1'))),
    # Auth URLs
    path('auth/token/', CustomTokenViewBase.as_view(), name='api-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api-refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='api-verify'),
]

# Non-versioned router
default_router = routers.SimpleRouter()
default_router.register(
    r'workspace', views.WorkspaceViewSet, basename='api-workspace')

# Chat URL patterns
chat_urlpatterns = [
    path('', views.chat, name="api-chat"),
]

# Documentation URLs
doc_patterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='services:schema'), name='swagger-ui'),
    path('schema/redoc/',
         SpectacularRedocView.as_view(url_name='services:schema'), name='redoc'),
]

# Main URL patterns
urlpatterns = [
    # Version 1 APIs
    path('v1/', include((v1_patterns, 'v1'))),
    # Non-versioned endpoints
    path('', include(default_router.urls)),
    path('chat/', include(chat_urlpatterns)),
    # Documentation endpoints
    path('docs/', include(doc_patterns)),
]
