import { useEffect, useState } from "react";
import { fetchTasks, updateTaskStatus } from "./api/tasks";
import CreateTaskForm from "./components/CreateTaskForm";

const STATUS_STYLES = {
  pending: "bg-gray-200 text-gray-800",
  in_progress: "bg-blue-200 text-blue-800",
  completed: "bg-green-200 text-green-800",
  blocked: "bg-red-200 text-red-800",
};

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function loadTasks() {
    try {
      setLoading(true);
      const data = await fetchTasks();
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleStatusChange(taskId, newStatus) {
    try {
      await updateTaskStatus(taskId, newStatus);
      loadTasks();
    } catch (err) {
      alert(err.message);
    }
  }

  useEffect(() => {
    loadTasks();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">
          Task Dependency Management
        </h1>

        <CreateTaskForm onCreated={loadTasks} />

        {loading && <p>Loading tasks…</p>}
        {error && <p className="text-red-500">{error}</p>}

        {!loading && !error && (
          <ul className="space-y-3">
            {tasks.map((task) => (
              <li
                key={task.id}
                className="bg-white p-4 rounded shadow flex justify-between items-center"
              >
                <div>
                  <div className="font-semibold">{task.title}</div>
                  <div className="text-sm text-gray-600">
                    {task.description}
                  </div>
                </div>

                <select
                  value={task.status}
                  onChange={(e) =>
                    handleStatusChange(task.id, e.target.value)
                  }
                  className={`px-2 py-1 rounded text-sm font-medium ${
                    STATUS_STYLES[task.status]
                  }`}
                >
                  <option value="pending">pending</option>
                  <option value="in_progress">in_progress</option>
                  <option value="completed">completed</option>
                  <option value="blocked">blocked</option>
                </select>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
