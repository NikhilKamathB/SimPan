import json
from typing import Union
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from workers.sdc import app as sdc_app
from workers.validators import ExchangeName, RoutingKey
from comfyui.utils import make_message_response, return_http_response, generate_celery_response


def index(request):
    return render(request, "comfyui/comfyui.html")


def carla_actor_generator(request) -> Union[HttpResponse, HttpResponseServerError]:
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("by_pass", True):
            return return_http_response(
                make_message_response("Bypassed the actor generation.")
            )
        result = sdc_app.send_task("generate_actor", args=[
                                   data], exchange=ExchangeName.SDC.value, routing_key=RoutingKey.SDC.value).get()
        return generate_celery_response(result)


def carla_synthetic_data_generator(request) -> Union[HttpResponse, HttpResponseServerError]:
    if request.method == "POST":
        result = sdc_app.send_task("generate_synthetic_data", args=[
                                 json.loads(request.body)], exchange=ExchangeName.SDC.value, routing_key=RoutingKey.SDC.value).get()
        return generate_celery_response(result)

def carla_synthetic_data_report_generator(request):
    if request.method == "POST":
        result = sdc_app.send_task("generate_synthetic_data_report", args=[
                                 json.loads(request.body)], exchange=ExchangeName.SDC.value, routing_key=RoutingKey.SDC.value).get()
        return generate_celery_response(result)
