from langgraph.graph import StateGraph, END
from state import CareerNavigatorState

from agents.skill_extract import read_resume, extract_skills_and_domain
from agents.job_requirement import analyze_job_requirements
from agents.skill_gap import skill_gap_agent
from agents.roadmap_generator import roadmap_generator_agent



def build_graph():
    graph = StateGraph(CareerNavigatorState)

    # Nodes
    graph.add_node("read_resume",read_resume)
    graph.add_node("extract_skills", extract_skills_and_domain)
    graph.add_node("analyze_job_requirements", analyze_job_requirements)
    graph.add_node("skill_gap_agent", skill_gap_agent)
    graph.add_node("generate_roadmap", roadmap_generator_agent)

    # Edges
    graph.set_entry_point("read_resume")
    graph.add_edge("read_resume", "extract_skills")
    graph.add_edge("extract_skills", "analyze_job_requirements")
    graph.add_edge("analyze_job_requirements", "skill_gap_agent")
    graph.add_edge("skill_gap_agent", "generate_roadmap")

    graph.add_edge("generate_roadmap", END)

    return graph.compile()