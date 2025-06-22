from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from tasks.models import Task
from users.serializers import UserSerializer


class TaskViewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'status', 'due_date', 'is_overdue']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date']

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.is_overdue:
            raise PermissionDenied("This task is already overdue.")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
