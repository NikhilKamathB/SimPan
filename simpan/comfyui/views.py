import json
from django.shortcuts import render
from workers.validators import Status
from workers.sdc import app as sdc_app
from django.http import HttpResponse, HttpResponseServerError


def index(request):
    return render(request, "comfyui/comfyui.html")

def carla_actor_generator(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("by_pass", True):
            return HttpResponse(
                json.dumps({
                    "message": "Actor generation by-passed."
                }),
                content_type="application/json")
        task = sdc_app.send_task("generate_actor", args=[data])
        result = task.get()
        if result["status"] == Status.OK.value:
            return HttpResponse(
                json.dumps(result),
                content_type="application/json"
            )
        return HttpResponseServerError(
            json.dumps(result),
            content_type="application/json"
        )

def carla_synthetic_data_generator(request):
    if request.method == "POST":
        task = sdc_app.send_task("generate_synthetic_data", args=[json.loads(request.body)])
        result = task.get()
        if result["status"] == Status.OK.value:
            return HttpResponse(
                json.dumps(result),
                content_type="application/json"
            )
        return HttpResponseServerError(
            json.dumps(result),
            content_type="application/json"
        )
