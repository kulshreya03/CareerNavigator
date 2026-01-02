import axios from "axios";
import { useState } from "react";

export default function UploadForm({ setRoadmap, setLoading }) {
  const [resume, setResume] = useState(null);
  const [targetRole, setTargetRole] = useState("");
  const [experience, setExperience] = useState("beginner");
  const [hours, setHours] = useState(8);

  const submitForm = async () => {
    if (!resume || !targetRole) {
      alert("Resume and target role are required");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("target_role", targetRole);
    formData.append("experience_level", experience);
    formData.append("availability_hours_per_week", hours);

    setLoading(true);

    try {
      const res = await axios.post(
        "http://localhost:8000/generate-roadmap",
        formData
      );
      setRoadmap(res.data.roadmap);
    } catch (err) {
      alert("Error generating roadmap");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow max-w-xl mx-auto mb-8">
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setResume(e.target.files[0])}
        className="mb-4"
      />

      <input
        type="text"
        placeholder="Target Role (e.g. Backend Developer)"
        className="w-full p-2 border rounded mb-3"
        value={targetRole}
        onChange={(e) => setTargetRole(e.target.value)}
      />

      <select
        className="w-full p-2 border rounded mb-3"
        value={experience}
        onChange={(e) => setExperience(e.target.value)}
      >
        <option value="beginner">Beginner</option>
        <option value="mid">Mid</option>
        <option value="advanced">Advanced</option>
      </select>

      <input
        type="number"
        className="w-full p-2 border rounded mb-4"
        placeholder="Hours per week"
        value={hours}
        onChange={(e) => setHours(e.target.value)}
      />

      <button
        onClick={submitForm}
        className="bg-blue-600 text-white px-4 py-2 rounded w-full hover:bg-blue-700"
      >
        Generate Roadmap
      </button>
    </div>
  );
}
