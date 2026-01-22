from core.models import TaskDependency


def detect_cycle(start_task_id, target_task_id):
    """
    Check if target_task_id is reachable from start_task_id.
    If yes, adding target -> start creates a circular dependency.
    """

    visited = set()
    path = []

    def dfs(current_id):
        visited.add(current_id)
        path.append(current_id)

        if current_id == target_task_id:
            return True

        dependencies = TaskDependency.objects.filter(
            task_id=current_id
        ).values_list("depends_on_id", flat=True)

        for dep_id in dependencies:
            if dep_id not in visited:
                if dfs(dep_id):
                    return True

        path.pop()
        return False

    has_cycle = dfs(start_task_id)

    if has_cycle:
        return True, path + [start_task_id]

    return False, []
