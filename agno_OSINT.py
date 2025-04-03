from agno.agent import Agent
from agno.models.gemini import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
import re
from dotenv import load_dotenv
import os

load_dotenv()

class OSINTFileFetcherTool:
    name = "OSINT File Fetcher"
    description = ("A tool that uses OSINT techniques to search the internet for files "
                   "(e.g., PDFs, DOCs, images) related to a person’s identity. "
                   "It leverages search operators (like filetype:) to narrow down results.")

    def run(self, query: str):
        ddg_tool = DuckDuckGoTools()
        found_files = []

        filetypes = ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "jpg", "png"]

        for ft in filetypes:
            search_query = f'"{query}" filetype:{ft}'
            results = ddg_tool.search(search_query)
            for result in results:
                url = result.get("url", "")
                if url.lower().endswith(ft):
                    found_files.append(url)
        
        return list(set(found_files))

osint_tool = OSINTFileFetcherTool()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

agent = Agent(
    model=Gemini(id="gemini-2.0-pro", api_key=GOOGLE_API_KEY),
    description=("You are an OSINT agent that fetches publicly available files related to a person's "
                 "digital identity using various OSINT techniques. Your task is to find and list URLs "
                 "of files (e.g., reports, images, documents) associated with the provided identity."),
    tools=[osint_tool],  
    show_tool_calls=True,
    markdown=True
)

if __name__ == "__main__":
    person_identity = "Elon Musk"  
    print(f"Searching for files related to: {person_identity}\n")
    
    file_results = osint_tool.run(person_identity)
    
    if file_results:
        print("Found the following file URLs:")
        for url in file_results:
            print(f" - {url}")
    else:
        print("No files found for the given identity.")