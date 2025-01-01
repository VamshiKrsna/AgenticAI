from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
# from phi.tools.newspaper4k import Newspaper4k
from dotenv import load_dotenv

load_dotenv()

web_search_agent = Agent( 
    name = "Web Searching Agent",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools = [DuckDuckGo()],
    instructions = "Always include the sources",
    show_tool_calls = True,
    markdown = True,
    debug_model = True
)

web_search_agent.print_response("Who is the ceo of Tesla ? ", stream = True)