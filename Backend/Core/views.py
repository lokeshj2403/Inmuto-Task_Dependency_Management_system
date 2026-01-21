from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Task, TaskDependency
from core.serializers import TaskSerializer
from core.services.dependency_checker import detect_cycle
from core.services.status_updater import (
    evaluate_task_status,
    cascade_status_update
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)

        task = self.get_object()
        if task.status == Task.STATUS_COMPLETED:
            cascade_status_update(task)

        return response

    @action(detail=True, methods=["post"])
    def dependencies(self, request, pk=None):
        task = self.get_object()
        depends_on_id = request.data.get("depends_on_id")

        if str(task.id) == str(depends_on_id):
            return Response(
                {"error": "Task cannot depend on itself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Build dependency graph
        dependency_map = {}
        for dep in TaskDependency.objects.all():
            dependency_map.setdefault(dep.task_id, []).append(dep.depends_on_id)

        has_cycle, path = detect_cycle(
            start_task_id=task.id,
            target_task_id=int(depends_on_id),
            dependency_map=dependency_map
        )

        if has_cycle:
            return Response(
                {
                    "error": "Circular dependency detected",
                    "path": path
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        TaskDependency.objects.create(
            task_id=task.id,
            depends_on_id=depends_on_id
        )

        evaluate_task_status(task)

        return Response(
            {"message": "Dependency added"},
            status=status.HTTP_201_CREATED
        )
