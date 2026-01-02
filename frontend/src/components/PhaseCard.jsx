import { CheckCircle, Circle } from "lucide-react";

export default function PhaseCard({ phase, index }) {
  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h3 className="text-xl font-bold mb-2">
        Phase {index + 1}: {phase.phase}
      </h3>

      <p className="text-gray-600 mb-2">
        ⏱ Duration: {phase.duration_weeks} weeks
      </p>

      <p className="mb-3">
        🎯 Focus Skills:{" "}
        <span className="font-medium">
          {phase.focus_skills.join(", ")}
        </span>
      </p>

      <ul className="space-y-2 mb-4">
        {phase.tasks.map((task) => (
          <li
            key={task.task_id}
            className="flex items-center gap-2 text-sm"
          >
            {task.status === "completed" ? (
              <CheckCircle className="text-green-500" size={18} />
            ) : (
              <Circle className="text-gray-400" size={18} />
            )}
            {task.description}
          </li>
        ))}
      </ul>

      <div className="text-sm bg-gray-100 p-3 rounded">
        🛠 Mini Project: <b>{phase.mini_project}</b>
      </div>
    </div>
  );
}
