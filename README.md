# CareerRoadmap — Agentic AI Career Navigator

A small system combining a FastAPI backend + React (Vite) frontend that ingests a resume (PDF) and generates a tailored career roadmap using LangChain/LangGraph agents.

## Features

- Upload a resume (PDF) and specify a target role
- Extract skills from resume and compare against job requirements
- Generate a multi-phase learning/roadmap with estimated time and milestones
- Simple REST API (FastAPI) and a React + Vite SPA frontend

## Architecture Overview

- Backend: Python (FastAPI) that hosts the API and invokes a LangGraph pipeline defined in `backend/graph.py`.
- Frontend: React app bootstrapped with Vite (in `frontend/`) that calls the backend endpoints.
- Uploads are stored in `backend/uploads/` during processing.

## Prerequisites

- Python 3.10+ (recommended)
- Node.js 18+ and npm (or yarn)
- Optional: Docker (if you prefer containerized runs)

## Quickstart — Backend (local)

1. From the project root, create a virtual environment and install deps:

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\\Scripts\\Activate.ps1
# Windows (cmd)
.venv\\Scripts\\activate.bat
# macOS / Linux
source .venv/bin/activate

pip install -r backend/requirements.txt
```

2. Run the FastAPI server with `uvicorn` (from project root):

```bash
# From project root (module path `backend.main:app`)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# OR, if you `cd backend` first:
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Health check:

```bash
curl http://127.0.0.1:8000/health
# -> {"status":"ok"}
```

Notes:
- The backend expects uploaded resumes as PDF files (see `backend/main.py`).
- Uploaded files are saved under `backend/uploads/`.

## Quickstart — Frontend

1. Install dependencies and run the dev server:

```bash
cd frontend
npm install
npm run dev
```

2. Open the app in the browser at the Vite dev URL (usually `http://localhost:5173`).

3. The frontend sends POST requests to the backend `/generate-roadmap` endpoint; ensure the backend is running and reachable.

## API Endpoints (summary)

- `POST /generate-roadmap` — multipart/form-data with:
  - `resume` (PDF file)
  - `target_role` (string)
  - `experience_level` (string) — optional, defaults to `beginner`
  - `availability_hours_per_week` (int) — optional, defaults to `8`

  Response contains generated `roadmap`, `skill_gap`, and `current_step` fields.

- `GET /health` — simple health check.

## Project Layout

- `backend/` — Python backend
  - `main.py` — FastAPI application and endpoints
  - `graph.py` — LangGraph pipeline builder
  - `state.py` — state schema/types
  - `agents/` — agent components used by the pipeline
  - `uploads/` — runtime resume uploads

- `frontend/` — React + Vite frontend
  - `src/` — app source

## Development Tips

- Environment variables: if you need API keys (e.g., for LLM providers), store them in a `.env` in `backend/` and load them with `python-dotenv`.
- Use CORS carefully when deploying — `backend/main.py` currently allows `*` origins for development.

## Running in Production

- Consider using a process manager (Gunicorn + Uvicorn workers) or containerization.
- Secure environment variables and restrict CORS to known origins.

## Contributing

1. Create an issue describing the change.
2. Open a pull request with clear tests or manual steps to validate.

## License

This repo does not include an explicit license file. Add one (e.g., MIT) if you plan to open-source it.

## Contact

For questions, run the app locally and open an issue in this repository with reproduction steps.
