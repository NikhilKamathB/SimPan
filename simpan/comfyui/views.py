import json
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "comfyui/comfyui.html")

def carla_synthetic_data_generator(request):
    if request.method == "POST":
        return HttpResponse(
            json.dumps({"message": "POST request received"}),
            content_type="application/json"
        )