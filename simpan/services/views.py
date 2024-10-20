from bs4 import BeautifulSoup
from markdown import markdown
from rest_framework import status
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from db.models import Workspace, WorkspaceStorage
from services.serializers import UserSerializer, WorkspaceSerializer
from services.validators import APIResponse, ChatResponse, BaseFileStruct, BaseErrorStruct


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
                    "workspace_id": "<ID>",
                    "chat_response": "<p>This is a chat response - in HTML format</p>",
                    "files": [
                        {
                            "id": "1",
                            "name": "file1.pdf",
                            "url": "http://localhost:8000/media/file1.pdf",
                            "type": "pdf"
                        },
                    ]
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
                    "code": 400,
                    "message": "Bad Request"
                }
            },
            response_only=True,
            status_codes=['400'],
        ),
        OpenApiExample(
            'Internal Server Error',
            value={
                "success": False,
                "message": "An error occurred",
                "data": {
                    "code": 500,
                    "message": "Internal Server Error"
                }
            },
            response_only=True,
            status_codes=['500'],
        ),
    ],
)
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def chat(request):
    try:
        query = request.POST.get("chat_query")
        if not query:
            raise BadRequest("You have not provided a query.")
        workspace_id = request.POST.get("workspace_id")
        workspace_obj, created = Workspace.objects.get_or_create(
            id=workspace_id)
        if created:
            request.session["workspace"] = str(workspace_obj.id)
        conversation = {
            "query": query,
        }
        for _, f in request.FILES.items():
            WorkspaceStorage.objects.create(
                workspace=workspace_obj, file=f).save()
        response = query
        response_html = markdown(response)
        soup = BeautifulSoup(response_html, 'html.parser')
        if soup.find_all() == [soup.p]:
            fomatted_response = response_html
        else:
            fomatted_response = f'<div class="chatbot-body-text-response-container">{response_html}</div>'
        conversation["response"] = fomatted_response
        if workspace_obj.conversation:
            workspace_obj.conversation.append(conversation)
        else:
            workspace_obj.conversation = [conversation]
        workspace_obj.save()
        files = None
        if request.FILES:
            workspace_updated_files_obj = WorkspaceStorage.objects.filter(
                workspace=workspace_obj)
            files = [
                BaseFileStruct(id=str(f.id), name=f.file.name,
                               url=f.file.url, type=f.file.name.split(".")[-1].lower())
                for f in workspace_updated_files_obj
            ]
        return JsonResponse(
            APIResponse(
                success=True, message="Chat response generated successfully",
                data=ChatResponse(
                    workspace_id=str(workspace_obj.id),
                    chat_response=fomatted_response,
                    files=files
                ).model_dump(),
            ).model_dump(),
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return JsonResponse(
            APIResponse(
                success=False, message="An error occurred",
                data=BaseErrorStruct(
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).model_dump(),
            ).model_dump(),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all users",
        description="Retrieve a list of all users",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "success": True,
                            "message": "User list API",
                            "data": [
                                {
                                    "id": "<ID>",
                                    "username": "<USERNAME>",
                                    "email": "<EMAIL>",
                                    "first_name": "<FIRST_NAME>",
                                    "last_name": "<LAST_NAME>",
                                    "is_active": "<IS_ACTIVE>",
                                    "is_staff": "<IS_STAFF>",
                                    "is_superuser": "<IS_SUPERUSER>"
                                }
                            ]
                        }
                    )
                ]
            )
        }
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return JsonResponse(
            APIResponse(
                success=True, message="User list API",
                data=response.data.serializer.data,
            ).model_dump(), status=response.status_code)


class WorkspaceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):

    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all workspaces",
        description="Retrieve a list of all workspaces",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "success": True,
                            "message": "Workspace list API",
                            "data": [
                                {
                                    "id": "<ID>",
                                    "workspace_files": [
                                        {
                                            "id": "<ID>",
                                            "file": "<FILE>",
                                            "created_at": "<CREATED_AT>",
                                            "updated_at": "<UPDATED_AT>",
                                            "workspace": "<WORKSPACE_ID>"
                                        }
                                    ],
                                    "conversation": [
                                        {
                                            "query": "<QUERY>",
                                            "response": "<RESPONSE>"
                                        }
                                    ],
                                    "name": "<NAME>",
                                    "created_at": "<CREATED_AT>",
                                    "updated_at": "<UPDATED_AT>",
                                    "user": "<USER>"
                                }
                            ]
                        }
                    )
                ]
            )
        }
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return JsonResponse(
            APIResponse(
                success=True, message="Workspace list API",
                data=response.data.serializer.data,
            ).model_dump(), status=response.status_code)

    @extend_schema(
        summary="Create a new workspace",
        description="Create a new workspace with a unique ID",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "success": True,
                            "message": "Workspace create API",
                            "data": {
                                "id": "<ID>",
                                "conversation": "null",
                                "name": "<NAME>",
                                "created_at": "<CREATED_AT>",
                                "updated_at": "<UPDATED_AT>",
                                "user": "<USER>"
                            }
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Error Response',
                        value={
                            "success": False,
                            "message": "An error occurred",
                            "data": {
                                "code": 500,
                                "message": "Internal Server Error"
                            }
                        }
                    )
                ]
            )
        }
    )
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return JsonResponse(
                APIResponse(
                    success=True, message="Workspace create API",
                    data=response.data.serializer.data,
                ).model_dump(), status=response.status_code)
        except Exception as e:
            return JsonResponse(
                APIResponse(
                    success=False, message="An error occurred while creating workspace",
                    data=BaseErrorStruct(
                        code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).model_dump(),
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Delete a workspace",
        description="Delete a workspace by ID",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "success": True,
                            "message": "Workspace delete API",
                        }
                    )
                ]
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return JsonResponse(
            APIResponse(
                success=True, message="Workspace delete API"
            ).model_dump(), status=response.status_code)
