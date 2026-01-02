from typing import TypedDict, List, Dict, Optional

class CareerNavigatorState(TypedDict):
    # User context
    user_id: str
    target_role: str
    experience_level: str
    availability_hours_per_week: int

    # Resume
    resume_path: str
    resume_text: str
    resume_skills: Dict[str, List[str]]

    # Job requirements
    job_requirements: Dict[str, List[str]]

    # Skill gap
    skill_gap: Dict[str, List[str]]

    # Roadmap
    roadmap: List[Dict]

    # Progress tracking
    progress_updates: List[Dict]

    # Evaluation
    evaluation_result: Optional[Dict]

    # Adaptive changes
    adaptive_changes: Optional[Dict]

    # Control flags
    current_step: str
    is_roadmap_generated: bool
    needs_revision: bool
