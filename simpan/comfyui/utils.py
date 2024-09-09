import json
from typing import Union
from workers.validators import Status
from workers.sdc import app as sdc_app
from simpan.validator import ResponseValidator
from comfyui.constants import SDC_TASK
from db.models import CeleryTask, CeleryTaskStatus
from workers.validators import ExchangeName, RoutingKey
from django.http import HttpResponse, HttpResponseServerError


def make_message_response(message: str, body: dict = None) -> dict:
    return ResponseValidator(
        message=message,
        body=body
    ).model_dump(mode="json")

def return_http_response(response: dict) -> HttpResponse:
    return HttpResponse(
        json.dumps(response),
        content_type="application/json")

def return_http_server_error(response: dict) -> HttpResponseServerError:
    return HttpResponseServerError(
        json.dumps(response),
        content_type="application/json"
    )

def generate_celery_response(result: dict) -> Union[HttpResponse, HttpResponseServerError]:
    if result["status"] == Status.OK.value:
        return return_http_response(result)
    return return_http_server_error(result)

def trigger_sdc_task(task_name: str, body: dict) -> dict:
    task = sdc_app.send_task(task_name, args=[body], exchange=ExchangeName.SDC.value, routing_key=RoutingKey.SDC.value)
    sdc_task_object = CeleryTask.objects.create(
        task_id=task.id,
        task_name=task_name,
        task_type=SDC_TASK,
        queue_name=ExchangeName.SDC.value
    )
    result = task.get()
    sdc_task_object.status = CeleryTaskStatus.COMPLETED
    sdc_task_object.save()
    return result