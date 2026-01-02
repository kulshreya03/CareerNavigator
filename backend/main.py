import os
import uuid
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from werkzeug.utils import secure_filename

from graph import build_graph
from state import CareerNavigatorState

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI(title="Agentic AI Career Navigator")

# -----------------------------
# CORS (IMPORTANT)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()

# -----------------------------
# Utility
# -----------------------------
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# API: Generate Roadmap
# -----------------------------
@app.post("/generate-roadmap")
async def generate_roadmap(
    resume: UploadFile = File(...),
    target_role: str = Form(...),
    experience_level: str = Form("beginner"),
    availability_hours_per_week: int = Form(8),
):
    """
    Expects multipart/form-data:
    - resume (PDF)
    - target_role (string)
    - experience_level (string)
    - availability_hours_per_week (int)
    """

    if not allowed_file(resume.filename):
        raise HTTPException(status_code=400, detail="Invalid resume file type")

    # Save resume
    filename = secure_filename(resume.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    resume_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    with open(resume_path, "wb") as f:
        f.write(await resume.read())

    # -----------------------------
    # Initial LangGraph State
    # -----------------------------
    initial_state: CareerNavigatorState = {
        "user_id": str(uuid.uuid4()),
        "resume_path": resume_path,
        "target_role": target_role,
        "experience_level": experience_level,
        "availability_hours_per_week": availability_hours_per_week,

        # Empty initial fields
        "resume_text": "",
        "resume_skills": {},
        "job_requirements": {},
        "skill_gap": {},
        "roadmap": [],
        "progress_updates": [],
        "evaluation_result": None,
        "adaptive_changes": None,
        "current_step": "start",
        "is_roadmap_generated": False,
        "needs_revision": False,
    }

    # -----------------------------
    # Run LangGraph
    # -----------------------------
    final_state = graph.invoke(initial_state)

    # -----------------------------
    # API Response
    # -----------------------------
    return JSONResponse(
        content={
            "user_id": final_state.get("user_id"),
            "target_role": target_role,
            "experience_level": experience_level,
            "roadmap": final_state.get("roadmap"),
            "skill_gap": final_state.get("skill_gap"),
            "current_step": final_state.get("current_step"),
        }
    )


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

'''
from state import CareerNavigatorState
from graph import build_graph

def run():
    graph = build_graph()

    initial_state = CareerNavigatorState(
        resume_path="resume.pdf",
        user_id="user_123",
        target_role="Backend Developer",
        experience_level="Mid",
        availability_hours_per_week=10,
        resume_text="",
        resume_skills={},
        job_requirements={},
        skill_gap={},
        roadmap=[],
    )

    final_state = graph.invoke(initial_state)
    print(final_state)

if __name__ == "__main__":
    run()
'''