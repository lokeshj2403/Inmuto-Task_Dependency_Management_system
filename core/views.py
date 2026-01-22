from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from core.models import Task, TaskDependency
from core.serializers import TaskSerializer
from core.services.status_updater import (
    evaluate_task_status,
    cascade_status_update,
)
from core.services.dependency_checker import detect_cycle


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        new_status = request.data.get("status")

        if new_status:
            task.status = new_status
            task.save(update_fields=["status"])

            # Cascade update to dependent tasks
            cascade_status_update(task)

        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def dependencies(self, request, pk=None):
        task = self.get_object()
        depends_on_id = request.data.get("depends_on_id")

        if not depends_on_id:
            return Response(
                {"error": "depends_on_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if task.id == depends_on_id:
            return Response(
                {"error": "Task cannot depend on itself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            depends_on = Task.objects.get(id=depends_on_id)
        except Task.DoesNotExist:
            return Response(
                {"error": "Dependency task does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 🔴 CORRECT CIRCULAR DEPENDENCY CHECK
        has_cycle, path = detect_cycle(
            start_task_id=depends_on.id,
            target_task_id=task.id,
        )

        if has_cycle:
            return Response(
                {
                    "error": "Circular dependency detected",
                    "path": path,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Safe to create dependency
        TaskDependency.objects.create(
            task=task,
            depends_on=depends_on,
        )

        # Recalculate task status after adding dependency
        evaluate_task_status(task)

        return Response(
            {"success": True},
            status=status.HTTP_201_CREATED,
        )
