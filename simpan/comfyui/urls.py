from django.urls import path
from comfyui import views

app_name = "comfyui"

urlpatterns = [
    path('', views.index, name="comfyui")
]
