import json
from typing import Union
from workers.validators import Status
from simpan.validator import ResponseValidator
from django.http import HttpResponse, HttpResponseServerError


def make_message_response(message: str) -> dict:
    return ResponseValidator(
        message=message
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