from langgraph.graph import StateGraph, END
from tavily_search import run_research_agent
from answer_drafter import run_draft_agent
from langsmith import traceable
import os
from dotenv import load_dotenv

load_dotenv()

def create_research_workflow():
    @traceable(name="Research Phase")
    def execute_research(state):
        result = run_research_agent(state["query"])
        return {
            "research_data": result["output"],
            "query": state["query"] 
        }
    
    @traceable(name="Drafting Phase")
    def execute_draft(state):
        return {
            "final_answer": run_draft_agent(
                state["research_data"],
                state["query"]
            ),
            "query": state["query"]  
        }
    
    builder = StateGraph(dict)
    builder.add_node("research", execute_research)
    builder.add_node("draft", execute_draft)
    builder.set_entry_point("research")
    builder.add_edge("research", "draft")
    builder.add_edge("draft", END)
    
    return builder.compile()

@traceable(name="Research Orchestrator")
def run_research_system(query):
    workflow = create_research_workflow()
    result = workflow.invoke({"query": query})
    return {
        "research_data": result.get("research_data", ""),
        "final_answer": result.get("final_answer", ""),
        "query": query
    }