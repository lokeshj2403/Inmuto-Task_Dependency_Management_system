def detect_cycle(start_task_id, target_task_id, dependency_map):
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        stack.append(node)

        for neighbor in dependency_map.get(node, []):
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
