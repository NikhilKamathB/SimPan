from django.urls import path
from comfyui import views

app_name = "comfyui"

urlpatterns = [
    path('', views.index, name="comfyui"),
    path("carla/actor-generator/", views.carla_actor_generator, name="carla_actor_generator"),
    path("carla/synthetic-data-generator/", views.carla_synthetic_data_generator, name="carla_synthetic_data_generator"),
    path("carla/synthetic-data-report-generator/", views.carla_synthetic_data_report_generator, name="carla_synthetic_data_report_generator"),
]
