from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from core.models import Task, TaskDependency
from core.serializers import TaskSerializer
from core.services.status_updater import (
    evaluate_task_status,
    cascade_status_update,
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        new_status = request.data.get("status")

        if new_status:
            task.status = new_status
            task.save(update_fields=["status"])

            # 🔥 THIS IS THE CRITICAL LINE
            cascade_status_update(task)

        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def dependencies(self, request, pk=None):
        task = self.get_object()
        depends_on_id = request.data.get("depends_on_id")

        if task.id == depends_on_id:
            return Response(
                {"error": "Task cannot depend on itself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        depends_on = Task.objects.get(id=depends_on_id)

        TaskDependency.objects.create(
            task=task,
            depends_on=depends_on
        )

        # Recalculate task status after adding dependency
        evaluate_task_status(task)

        return Response({"success": True})
