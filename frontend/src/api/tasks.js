const BASE_URL = "http://127.0.0.1:8000/api";

export async function fetchTasks() {
  const res = await fetch(`${BASE_URL}/tasks/`);
  if (!res.ok) {
    throw new Error("Failed to fetch tasks");
  }
  return res.json();
}
export async function updateTaskStatus(taskId, status) {
  const res = await fetch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });

  if (!res.ok) {
    throw new Error("Failed to update task status");
  }

  return res.json();
}