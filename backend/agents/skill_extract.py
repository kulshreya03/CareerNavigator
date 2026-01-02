import pdfplumber
import json
import re
from langchain_core.messages import HumanMessage
from typing import Dict, List

from state import CareerNavigatorState
from llm import llm

import os

# -----------------------------
# Resume Reader Agent
# -----------------------------
def read_resume(state: CareerNavigatorState) -> CareerNavigatorState:
    """
    Reads resume PDF and stores extracted text in state
    """
    resume_path = state["resume_path"]

    #if not resume_path:
     #   state["resume_text"] = ""
      #  return state
    print("CWD:", os.getcwd())
    print("Resume path:", resume_path)
    print("Exists:", os.path.exists(resume_path))
    print("Is file:", os.path.isfile(resume_path))

    with pdfplumber.open(resume_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    print("Resume text length:", len(text))

    state["resume_text"] = text
    return state


# -----------------------------
# Skill Extraction Agent
# -----------------------------
def extract_skills_and_domain(state: CareerNavigatorState) -> CareerNavigatorState:
    """
    Extracts categorized skills and professional domain from resume text
    """

    resume_text = state.get("resume_text", "")

    if not resume_text:
        state["resume_skills"] = {}
        state["domain"] = ""
        return state

    prompt = f"""
You are an expert resume parsing AI.

STRICT RULES:
- Return ONLY valid raw JSON
- No markdown
- No explanations
- All fields must exist
- Skill names must be concise and normalized

Extract:
1. Categorized technical skills
2. Primary professional domain (specific role/domain)

Resume Text:
{resume_text}

Return EXACT JSON:
{{
  "skills": {{
    "languages": [],
    "frameworks": [],
    "databases": [],
    "cloud": [],
    "tools": [],
    "concepts": []
  }},
  "domain": ""
}}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = re.sub(r"```json|```", "", response.content).strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        state["resume_skills"] = {}
        state["domain"] = ""
        state["current_step"] = "skill_extraction_failed"
        return state

    # Normalize skills
    normalized_skills = normalize_skills(data.get("skills", {}))

    state["resume_skills"] = normalized_skills
    state["domain"] = data.get("domain", "").strip()
    state["current_step"] = "skills_extracted"

    return state


# -----------------------------
# Skill Normalization Utility
# -----------------------------
def normalize_skills(skills: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Normalizes skill names to avoid duplicates and inconsistencies
    """

    normalization_map = {
        "js": "JavaScript",
        "node": "Node.js",
        "node js": "Node.js",
        "express js": "Express",
        "mongodb atlas": "MongoDB",
        "aws ec2": "AWS",
        "docker container": "Docker"
    }

    normalized = {}

    for category, values in skills.items():
        cleaned = set()
        for skill in values:
            key = skill.lower().strip()
            cleaned.add(normalization_map.get(key, skill.strip()))
        normalized[category] = sorted(cleaned)

    return normalized
