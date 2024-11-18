
from rest_framework import status
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from workspace.models import Studio
from base.validators import APIResponse, BaseErrorStruct
from workspace.api.v1.serializers import StudioSerializerV1


@extend_schema(tags=["Studio"])
class StudioViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):

    queryset = Studio.objects.all()
    serializer_class = StudioSerializerV1
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all studios",
        description="Retrieve a list of all studios",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "success": True,
                            "message": "<LIST_API_MESSAGE>",
                            "data": [
                                {
                                    "id": "<ID>",
                                    "studio_files": [
                                        {
                                            "id": "<ID>",
                                            "file": "<FILE>",
                                            "created_at": "<CREATED_AT>",
                                            "updated_at": "<UPDATED_AT>",
                                            "studio": "<STUDIO_ID>"
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
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Error Response',
                        value={
                            "success": False,
                            "message": "<GENERIC_ERROR_MESSAGE>",
                            "data": {
                                "code": 500,
                                "message": "<MESSAGE>"
                            }
                        }
                    )
                ]
            )
        }
    )
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return JsonResponse(
            APIResponse(
                success=True, message="Studio list API",
                    data=response.data.serializer.data,
                ).model_dump(), status=response.status_code)
        except Exception as e:
            return JsonResponse(
                APIResponse(
                    success=False, message="An error occurred while listing studios",
                    data=BaseErrorStruct(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).model_dump(),
                ).model_dump(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Create a new studio",
        description="Create a new studio with a unique ID",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "success": True,
                            "message": "<CREATE_API_MESSAGE>",
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
                            "message": "<GENERIC_ERROR_MESSAGE>",
                            "data": {
                                "code": 500,
                                "message": "<MESSAGE>"
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
                    success=True, message="Created studio",
                    data=response.data.serializer.data,
                ).model_dump(), status=response.status_code)
        except Exception as e:
            return JsonResponse(
                APIResponse(
                    success=False, message="An error occurred while creating studio",
                    data=BaseErrorStruct(
                        code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).model_dump(),
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Delete a studio",
        description="Delete a studio by ID",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "success": True,
                            "message": "<DELETE_API_MESSAGE>",
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
                            "message": "<GENERIC_ERROR_MESSAGE>",
                            "data": {
                                "code": 500,
                                "message": "<MESSAGE>"
                            }
                        }
                    )
                ]
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return JsonResponse(
            APIResponse(
                success=True, message="Deleted studio"
            ).model_dump(), status=response.status_code)
        except Exception as e:
            return JsonResponse(
                APIResponse(
                    success=False, message="An error occurred while deleting studio",
                    data=BaseErrorStruct(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).model_dump(),
                ).model_dump(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
