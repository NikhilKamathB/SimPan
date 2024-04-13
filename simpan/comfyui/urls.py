from django.urls import path
from comfyui import views

app_name = "comfyui"

urlpatterns = [
    path('', views.index, name="comfyui"),
    path("carla/synthetic-data-generator/", views.carla_synthetic_data_generator, name="carla_synthetic_data_generator"),
]
