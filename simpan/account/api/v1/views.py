
from rest_framework import status
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from account.serializers import UserSerializer
from base.validators import APIResponse, BaseErrorStruct


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
                success=True, message="User list API",
                    data=response.data.serializer.data,
                ).model_dump(), status=response.status_code)
        except Exception as e:
            return JsonResponse(
                APIResponse(
                    success=False, message="An error occurred while listing users",
                    data=BaseErrorStruct(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).model_dump(),
                ).model_dump(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomTokenViewBase(TokenObtainPairView):

    """
    Create a new token for authentication
    """

    @extend_schema(
        summary="Create a new token",
        description="Generate a new access and refresh token for authentication",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "success": True,
                            "message": "<TOKEN_CREATE_MESSAGE>",
                            "data": {
                                "access": "<ACCESS_TOKEN>",
                                "refresh": "<REFRESH_TOKEN>"
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
    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            response = Response(serializer.validated_data, status=status.HTTP_200_OK)
            return JsonResponse(
                APIResponse(
                    success=True, message="Token create API",
                    data=response.data,
                ).model_dump(), status=response.status_code)
        except Exception as e:
            return JsonResponse(
                APIResponse(
                    success=False, message="An error occurred while creating token",
                    data=BaseErrorStruct(
                        code=status.HTTP_400_BAD_REQUEST, message=str(e)).model_dump(),
                ).model_dump(),
                status=status.HTTP_400_BAD_REQUEST
            )