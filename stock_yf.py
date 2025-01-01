from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

web_search_agent = Agent( 
    name = "Web Searching Agent",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools = [YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True,)],
    instructions = ["Use Tables to display the data"],
    show_tool_calls = True,
    markdown = True,
)

web_search_agent.print_response("summarize analyst recommendations and company news for NVDA", stream = True)