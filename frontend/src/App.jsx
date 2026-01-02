import { useState } from "react";
import UploadForm from "./components/UploadForm";
import RoadmapTimeline from "./components/RoadmapTimeline";
import Loader from "./components/Loader";

function App() {
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="min-h-screen p-6">
      <h1 className="text-3xl font-bold text-center mb-6">
        🚀 Agentic AI Career Navigator
      </h1>

      <UploadForm setRoadmap={setRoadmap} setLoading={setLoading} />

      {loading && <Loader />}

      {roadmap && <RoadmapTimeline roadmap={roadmap} />}
    </div>
  );
}

export default App;
