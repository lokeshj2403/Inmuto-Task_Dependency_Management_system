from collections import defaultdict

def detect_cycle(start_task_id, target_task_id, dependency_map):
    """
    Checks if adding an edge start_task -> target_task creates a cycle.

    Returns:
        (has_cycle: bool, path: list[int])
    """

    visited = set()
    stack = []

    def dfs(current):
        visited.add(current)
        stack.append(current)

        for neighbor in dependency_map.get(current, []):
            if neighbor == start_task_id:
                return True
            if neighbor not in visited:
                if dfs(neighbor):
                    return True

        stack.pop()
        return False

    if dfs(target_task_id):
        return True, stack + [start_task_id]

    return False, []
