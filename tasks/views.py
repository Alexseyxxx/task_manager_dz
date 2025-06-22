from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from tasks.models import Task
from tasks.serializers import TaskSerializer, TaskViewSerializer


class TaskViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search in title", type=openapi.TYPE_STRING),
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by due_date or -due_date", type=openapi.TYPE_STRING),
        ],
        responses={200: TaskViewSerializer(many=True)}
    )
    def list(self, request):
        tasks = request.user.user_tasks.all()

        if search := request.query_params.get('search'):
            tasks = tasks.filter(title__icontains=search)

        if status_filter := request.query_params.get('status'):
            tasks = tasks.filter(status=status_filter)

        if ordering := request.query_params.get('ordering'):
            if ordering in ['due_date', '-due_date']:
                tasks = tasks.order_by(ordering)

        serializer = TaskViewSerializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TaskSerializer, responses={201: TaskViewSerializer})
    def create(self, request):
        serializer = TaskSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskViewSerializer(task).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: TaskViewSerializer, 404: "Not Found"})
    def retrieve(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        return Response(TaskViewSerializer(task).data)

    @swagger_auto_schema(request_body=TaskSerializer)
    def update(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        if task.user != request.user:
            raise PermissionDenied("This task is not yours.")
        serializer = TaskSerializer(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Task updated", status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TaskSerializer)
    def partial_update(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        if task.user != request.user:
            raise PermissionDenied("This task is not yours.")
        serializer = TaskSerializer(instance=task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Task updated", status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: "Task deleted", 403: "Forbidden", 404: "Not Found"})
    def destroy(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        if task.user != request.user:
            raise PermissionDenied("This task is not yours.")
        task.delete()
        return Response("Task deleted", status=status.HTTP_200_OK)
