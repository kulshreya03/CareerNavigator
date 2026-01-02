import json
import re
from langchain_core.messages import HumanMessage

from state import CareerNavigatorState
from llm import llm


def roadmap_generator_agent(state: CareerNavigatorState) -> CareerNavigatorState:
    """
    Generates a structured, time-based learning roadmap
    based on identified skill gaps and user constraints.
    """

    skill_gap = state.get("skill_gap", {})
    experience_level = state.get("experience_level", "beginner")
    hours_per_week = state.get("availability_hours_per_week", 8)
    target_role = state.get("target_role", "")

    if not skill_gap:
        state["roadmap"] = []
        state["current_step"] = "roadmap_failed"
        return state

    prompt = f"""
You are an expert technical mentor and curriculum designer.

STRICT RULES:
- Return ONLY valid raw JSON
- No markdown
- No explanations
- All fields must exist
- Tasks must be practical and measurable
- Roadmap must be realistic for the given hours/week

USER CONTEXT:
Target Role: {target_role}
Experience Level: {experience_level}
Available Time: {hours_per_week} hours/week

SKILL GAPS:
Missing Skills: {skill_gap.get("missing_skills", [])}
Partial Skills: {skill_gap.get("partial_skills", [])}
Strong Skills: {skill_gap.get("strong_skills", [])}

Create a roadmap broken into phases.

Return EXACT JSON:
{{
  "roadmap": [
    {{
      "phase": "",
      "duration_weeks": 0,
      "focus_skills": [],
      "tasks": [
        {{
          "task_id": "",
          "description": "",
          "estimated_hours": 0,
          "evidence_required": "",
          "status": "pending"
        }}
      ],
      "mini_project": ""
    }}
  ]
}}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = re.sub(r"```json|```", "", response.content).strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        state["roadmap"] = []
        state["current_step"] = "roadmap_failed"
        return state

    state["roadmap"] = data.get("roadmap", [])
    state["is_roadmap_generated"] = True
    state["current_step"] = "roadmap_generated"

    print("RAW LLM OUTPUT:", response.content)

    return state
