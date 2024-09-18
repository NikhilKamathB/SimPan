from django.urls import path
from comfychat import views

app_name = "comfychat"

urlpatterns = [
    path('', views.index, name="comfychat"),
    path('delete_workspace/', views.delete_workspace, name="delete_workspace"),
]