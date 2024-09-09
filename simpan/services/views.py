from markdown import markdown
from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import BadRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiExample
from services.validators import APIResponse, ChatResponse, BaseError


@extend_schema(
    summary="Chat API",
    description="Process a chat query and return a response",
    methods=['POST'],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'chat_query': {'type': 'string'},
                'workspace_id': {'type': 'string'},
                'files': {
                    'type': 'array',
                    'items': {'type': 'string', 'format': 'binary'},
                },
            },
            'required': ['chat_query'],
        },
    },
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
        500: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            'Sample Input',
            summary='Example chat query input',
            description='A typical request to the Chat API',
            value={
                "chat_query": "Thats life, thats what all the people say",
                "workspace_id": "ws_12345",
                "files": ["(binary)", "(binary)", "(binary)"]
            },
            request_only=True,
        ),
        OpenApiExample(
            'Successful Response',
            value={
                "success": True,
                "message": "Success",
                "data": {
                    "chatResponse": "<p>This is a chat response - in HTML format</p>"
                }
            },
            response_only=True,
            status_codes=['200'],
        ),
        OpenApiExample(
            'Error Response',
            value={
                "success": False,
                "message": "An error occurred",
                "data": {
                    "code": 500,
                    "message": "Internal Server Error"
                }
            },
            response_only=True,
            status_codes=['400', '500'],
        ),
    ],
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def chat(request):
    try:
        query = request.POST.get("chat_query")
        if not query:
            raise BadRequest("You have not provided a query.")
        workspace_id = request.POST.get("workspace_id")
        uploaded_files = request.FILES.getlist("files")
        response_html = markdown(query)
        return JsonResponse(
            APIResponse(
                success=True, message="Chat response generated successfully",
                data=ChatResponse(chatResponse=response_html).model_dump(),
            ).model_dump(),
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return JsonResponse(
            APIResponse(
                success=False, message="An error occurred",
                data=BaseError(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).model_dump(),
            ).model_dump(),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )