from django.urls import path
from comfychat import views

app_name = "comfychat"

urlpatterns = [
    path('', views.index, name="comfychat"),
]