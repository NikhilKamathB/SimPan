from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import BadRequest
from comfychat.validators import ChatAPIResponse


def post_chat_view_handler(func):
    def wrapper(request, *args, **kwargs):
        if request.method == "POST":
            try:
                return func(request, *args, **kwargs)
            except BadRequest as e:
                return JsonResponse(
                    ChatAPIResponse(success=False, message="Bad Request",
                                 description=f"{e}").model_dump(),
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return JsonResponse(
                    ChatAPIResponse(success=False, message="Internal Server Error",
                                 description=f"{e}").model_dump(),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return JsonResponse(
            ChatAPIResponse(success=False, message="Method not allowed",
                         description="This method is not allowed.").model_dump(),
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    return wrapper