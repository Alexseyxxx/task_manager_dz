from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from users.serializers import UserSerializer


class UserViewSet(ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def list(self, request: Request) -> Response:
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: "User successfully created", 400: "Validation error", 409: "Conflict"}
    )
    def create(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
