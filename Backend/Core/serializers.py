from rest_framework import serializers
from core.models import Task, TaskDependency

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskDependencySerializer(serializers.ModelSerializer):
    depends_on_id = serializers.IntegerField()

    class Meta:
        model = TaskDependency
        fields = ("id", "depends_on_id", "created_at")
