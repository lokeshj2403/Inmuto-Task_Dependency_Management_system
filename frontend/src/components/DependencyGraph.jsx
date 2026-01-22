export default function DependencyGraph({ tasks }) {
  const nodeWidth = 140;
  const nodeHeight = 50;
  const gapX = 200;
  const gapY = 80;

  // Simple vertical layout
  const positions = {};
  tasks.forEach((task, index) => {
    positions[task.id] = {
      x: 50 + Math.floor(index / 5) * gapX,
      y: 50 + (index % 5) * gapY,
    };
  });

  const STATUS_COLORS = {
    pending: "#e5e7eb",
    in_progress: "#bfdbfe",
    completed: "#bbf7d0",
    blocked: "#fecaca",
  };

  return (
    <svg width="100%" height="400" className="border mt-6 bg-white">
      {/* Arrows */}
      {tasks.map((task) =>
        task.dependencies?.map((dep) => {
          const from = positions[dep.depends_on];
          const to = positions[task.id];
          if (!from || !to) return null;

          return (
            <line
              key={`${task.id}-${dep.depends_on}`}
              x1={from.x + nodeWidth}
              y1={from.y + nodeHeight / 2}
              x2={to.x}
              y2={to.y + nodeHeight / 2}
              stroke="#555"
              markerEnd="url(#arrow)"
            />
          );
        })
      )}

      {/* Arrow marker */}
      <defs>
        <marker
          id="arrow"
          markerWidth="10"
          markerHeight="10"
          refX="6"
          refY="3"
          orient="auto"
        >
          <path d="M0,0 L0,6 L9,3 z" fill="#555" />
        </marker>
      </defs>

      {/* Nodes */}
      {tasks.map((task) => {
        const pos = positions[task.id];
        return (
          <g key={task.id}>
            <rect
              x={pos.x}
              y={pos.y}
              width={nodeWidth}
              height={nodeHeight}
              rx="8"
              fill={STATUS_COLORS[task.status]}
              stroke="#333"
            />
            <text
              x={pos.x + nodeWidth / 2}
              y={pos.y + nodeHeight / 2}
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize="12"
            >
              {task.title}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
