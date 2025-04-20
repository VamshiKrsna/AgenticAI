# uses Tavily to research about the topic and gather knowledge
import os 
from dotenv import load_dotenv
from tavily import TavilyClient 
from langchain_tavily import TavilySearch 
from langgraph import Graph, Node 
import argparse

load_dotenv() 

tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY")) 
tavily_tool = TavilySearch(tavily_client = tavily) 

# knowledge graph : 
graph = Graph(name = "research_graph")

def collect_index(topic: str, top_k: int = 5):
    """
    search web, collect and index top_k results into langgraph
    Args:
        topic (str): The topic to research about
        top_k (int): Number of top results to collect, defaults to 5
    """
    try:
        # Initialize the source node for the topic
        source_node = Node(id=topic, data={"type": "topic"})
        graph.add_node(source_node)

        results = tavily_tool.run(topic, top_k)
        for index, result in enumerate(results):
            node = Node(
                id = f"{topic}_{index}",
                data = {
                    "title": result["title"],
                    "url": result["url"],
                    "snippet": result["answer"] or result["content_snippet"]
                }
            )
            graph.add_node(node) 
            graph.add_edge(
                source = topic, 
                target = node.id, 
                metadata = {
                    "type":"found_in"
                }
            )
        graph.save("graph.json")
        print(f"Indexed {len(results)} results for '{topic}' into graph.json")
    except Exception as e:
        print(f"Error occurred while collecting data: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, help="topic to research about", required=True)
    parser.add_argument("--top_k", type=int, help="number of top results to collect", default=5)
    args = parser.parse_args()
    collect_index(args.topic, args.top_k)