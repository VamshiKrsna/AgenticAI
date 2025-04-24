from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessageGraph
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv() 

def create_drafting_workflow():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.4,
        convert_system_message_to_human=True
    ) # limited creativity for some juice
    
# what happened in pahalgam yesterday ? 

    def analyze_research(state):
        messages = [
            SystemMessage(content="Research Analyst"),
            HumanMessage(content=f"Analyze this data:\n{state['research_data']}")
        ]
        analysis = llm.invoke(messages).content
        return {"analysis": analysis, **state}

    def draft_answer(state):
        messages = [
            SystemMessage(content="Technical Writer"),
            HumanMessage(
                content=f"Create answer from:\nAnalysis: {state['analysis']}\nQuery: {state['query']}"
            )
        ]
        final = llm.invoke(messages).content
        return {"final_answer": final, **state}

    builder = MessageGraph()
    builder.add_node("analyze", analyze_research)
    builder.add_node("draft", draft_answer)
    builder.add_edge("analyze", "draft")
    builder.set_entry_point("analyze")
    builder.set_finish_point("draft")
    
    return builder.compile()

def run_draft_agent(research_data, query):
    workflow = create_drafting_workflow()
    result = workflow.invoke({
        "research_data": research_data,
        "query": query,
        "analysis": ""  # Initialize analysis field
    })
    return result.get("final_answer", "No answer generated")