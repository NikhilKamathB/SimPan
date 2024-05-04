import json
from typing import Union
from django.shortcuts import render
from celery.exceptions import TaskRevokedError
from django.http import HttpResponse, HttpResponseServerError
from comfyui.models import CeleryTask
from workers.sdc import app as sdc_app
from comfyui.constants import INITIATED, ABORTED
from comfyui.utils import make_message_response, return_http_response, generate_celery_response, trigger_sdc_task


def index(request):
    return render(request, "comfyui/comfyui.html")

def carla_actor_generator(request) -> Union[HttpResponse, HttpResponseServerError]:
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("by_pass", True):
            return return_http_response(
                make_message_response("Bypassed the actor generation.")
            )
        try:
            result = trigger_sdc_task("generate_actor", data)
        except TaskRevokedError:
            return return_http_response(
                make_message_response("Actor generation task aborted!", body={"trigger": False})
            )
        return generate_celery_response(result)

def carla_synthetic_data_generator(request) -> Union[HttpResponse, HttpResponseServerError]:
    if request.method == "POST":
        try:
            result = trigger_sdc_task("generate_synthetic_data", json.loads(request.body))
        except TaskRevokedError:
            return return_http_response(
                make_message_response(
                    "Synthetic data generation task aborted!", body={"trigger": False})
            )
        return generate_celery_response(result)

def carla_synthetic_data_report_generator(request):
    if request.method == "POST":
        try:
            result = trigger_sdc_task("generate_synthetic_data_report", json.loads(request.body))
        except TaskRevokedError:
            return return_http_response(
                make_message_response(
                    "Synthetic data report generation task aborted!", body={"trigger": False})
            )
        return generate_celery_response(result)

def abort(request):
    if request.method == "DELETE":
        tasks = CeleryTask.objects.filter(status=INITIATED)
        for task in tasks:
            sdc_app.control.revoke(task.task_id, terminate=True)
        tasks.update(status=ABORTED)
        return return_http_response(
            make_message_response("Task aborted successfully.")
        )