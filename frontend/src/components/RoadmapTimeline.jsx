import PhaseCard from "./PhaseCard";

export default function RoadmapTimeline({ roadmap }) {
  return (
    <div className="max-w-5xl mx-auto">
      <h2 className="text-2xl font-semibold mb-6">📍 Your Learning Roadmap</h2>

      <div className="space-y-6">
        {roadmap.map((phase, idx) => (
          <PhaseCard key={idx} phase={phase} index={idx} />
        ))}
      </div>
    </div>
  );
}
