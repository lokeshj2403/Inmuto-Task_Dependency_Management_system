from core.models import Task, TaskDependency


def evaluate_task_status(task):
    """
    Recalculate a task's status based on its dependencies.
    """
    dependencies = (
        TaskDependency.objects
        .filter(task=task)
        .select_related("depends_on")
    )

    # If no dependencies, do not auto-change status
    if not dependencies.exists():
        return

    statuses = [dep.depends_on.status for dep in dependencies]

    if any(status == Task.STATUS_BLOCKED for status in statuses):
        new_status = Task.STATUS_BLOCKED
    elif all(status == Task.STATUS_COMPLETED for status in statuses):
        new_status = Task.STATUS_IN_PROGRESS
    else:
        new_status = Task.STATUS_PENDING

    if task.status != new_status:
        task.status = new_status
        task.save(update_fields=["status"])


def cascade_status_update(task):
    """
    Recursively update all tasks that depend on the given task.
    """
    dependents = (
        TaskDependency.objects
        .filter(depends_on=task)
        .select_related("task")
    )

    for dep in dependents:
        dependent_task = dep.task

        # Recalculate dependent task
        evaluate_task_status(dependent_task)

        # CRITICAL FIX: recurse further
        cascade_status_update(dependent_task)
