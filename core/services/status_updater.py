from core.models import Task, TaskDependency


def evaluate_task_status(task):
    dependencies = TaskDependency.objects.filter(task=task).select_related("depends_on")

    if not dependencies.exists():
        return

    statuses = [d.depends_on.status for d in dependencies]

    if any(s == Task.STATUS_BLOCKED for s in statuses):
        new_status = Task.STATUS_BLOCKED
    elif all(s == Task.STATUS_COMPLETED for s in statuses):
        new_status = Task.STATUS_IN_PROGRESS
    else:
        new_status = Task.STATUS_PENDING

    if task.status != new_status:
        task.status = new_status
        task.save(update_fields=["status"])


def cascade_status_update(task):
    dependents = TaskDependency.objects.filter(depends_on=task).select_related("task")

    for dep in dependents:
        evaluate_task_status(dep.task)
