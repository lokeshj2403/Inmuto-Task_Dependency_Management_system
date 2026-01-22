import { useState } from "react";
import { addDependency } from "../api/tasks";

export default function AddDependency({ task, allTasks, onSuccess }) {
  const [selected, setSelected] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleAdd() {
    if (!selected) return;

    setLoading(true);
    setError(null);

    try {
      await addDependency(task.id, Number(selected));
      onSuccess();
      setSelected("");
    } catch (err) {
      if (err?.error) {
        setError(err);
      } else {
        setError({ error: "Failed to add dependency" });
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mt-2 flex items-center gap-2">
      <select
        value={selected}
        onChange={(e) => setSelected(e.target.value)}
        className="border px-2 py-1 text-sm rounded"
      >
        <option value="">Add dependency…</option>
        {allTasks
          .filter((t) => t.id !== task.id)
          .map((t) => (
            <option key={t.id} value={t.id}>
              {t.title}
            </option>
          ))}
      </select>

      <button
        onClick={handleAdd}
        disabled={!selected || loading}
        className="text-sm bg-gray-800 text-white px-2 py-1 rounded disabled:opacity-50"
      >
        Add
      </button>

      {error && (
        <div className="text-sm text-red-600 mt-1">
          <div>{error.error}</div>
          {error.path && (
            <div className="text-xs">
              Cycle: {error.path.join(" → ")}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
