from typing import Dict, List, Set
from state import CareerNavigatorState


def skill_gap_agent(state: CareerNavigatorState) -> CareerNavigatorState:
    """
    Compares resume skills with job requirements
    and identifies skill gaps
    """

    resume_skills = state.get("resume_skills", {})
    job_requirements = state.get("job_requirements", {})

    if not resume_skills or not job_requirements:
        state["skill_gap"] = {}
        state["current_step"] = "skill_gap_failed"
        return state

    resume_skill_set = flatten_skills(resume_skills)

    must_have = set(job_requirements.get("must_have", []))
    good_to_have = set(job_requirements.get("good_to_have", []))
    concepts = set(job_requirements.get("concepts", []))

    missing_skills = sorted(list(must_have - resume_skill_set))
    partial_skills = sorted(list((good_to_have | concepts) - resume_skill_set))
    strong_skills = sorted(list(resume_skill_set & (must_have | good_to_have)))

    state["skill_gap"] = {
        "missing_skills": missing_skills,
        "partial_skills": partial_skills,
        "strong_skills": strong_skills
    }

    state["current_step"] = "skill_gap_identified"
    return state


def flatten_skills(skills: Dict[str, List[str]]) -> Set[str]:
    """
    Converts categorized resume skills into a flat set
    """
    flat = set()
    for values in skills.values():
        for skill in values:
            flat.add(skill.strip())
    return flat
