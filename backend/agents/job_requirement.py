import json
import re
from langchain_core.messages import HumanMessage

from state import CareerNavigatorState
from llm import llm


def analyze_job_requirements(state: CareerNavigatorState) -> CareerNavigatorState:
    """
    Analyzes job requirements for the given target role and domain
    """

    target_role = state.get("target_role", "")
    domain = state.get("domain", "")

    if not target_role:
        state["job_requirements"] = {}
        state["current_step"] = "job_requirement_failed"
        return state

    prompt = f"""
You are an expert technical recruiter and career advisor AI.

STRICT RULES:
- Return ONLY valid raw JSON
- No markdown
- No explanations
- All fields must exist
- Skill names must be normalized and concise

TASK:
Identify the technical job requirements for the role.

Role: {target_role}
Domain: {domain}

Return EXACT JSON:
{{
  "must_have": [],
  "good_to_have": [],
  "concepts": []
}}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = re.sub(r"```json|```", "", response.content).strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        state["job_requirements"] = {}
        state["current_step"] = "job_requirement_failed"
        return state

    # Normalize requirements
    normalized_requirements = normalize_requirements(data)

    state["job_requirements"] = normalized_requirements
    state["current_step"] = "job_requirements_extracted"

    return state


def normalize_requirements(requirements: dict) -> dict:
    """
    Normalizes job requirement skill names
    """

    normalization_map = {
        "js": "JavaScript",
        "node js": "Node.js",
        "express js": "Express",
        "spring": "Spring Boot",
        "mysql db": "MySQL",
        "postgres": "PostgreSQL",
        "aws ec2": "AWS",
        "rest api": "REST APIs",
        "ci cd": "CI/CD"
    }

    normalized = {}

    for category, skills in requirements.items():
        cleaned = set()
        for skill in skills:
            key = skill.lower().strip()
            cleaned.add(normalization_map.get(key, skill.strip()))
        normalized[category] = sorted(cleaned)

    return normalized
