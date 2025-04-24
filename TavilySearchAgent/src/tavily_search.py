from langchain.agents import AgentExecutor 
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages 
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv() 
 
def create_reserach_agent():
    tools = [
        TavilySearchResults(
            api_key = os.getenv("TAVILY_API_KEY"),
            max_results = 3, 
            name = "crawler"
        )
    ]
    llm = ChatGoogleGenerativeAI(
        model = "gemini-1.5-flash",
        google_api_key = os.getenv("GEMINI_API_KEY"),
        temperature = 0,
    )# we need accurate, non hallucinating answers 
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user", """You are a senior research analyst. 
                Gather comprehensive information about: {input}.
                Use multiple search queries if needed.
                Validate sources and prioritize most recent data.
                Answer in third person perspective like a news reporter.
                """
            )
        ]
    )
    agent = (
        {
            "input":lambda x:x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
        }
        | prompt
        | llm.bind_tools(tools = tools)
        | OpenAIToolsAgentOutputParser()
    )
    return AgentExecutor(agent = agent, tools = tools)

def run_research_agent(query):
    executor = create_reserach_agent() 
    return executor.invoke(
        {
            "input":query
        }
    )