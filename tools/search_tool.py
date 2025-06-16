from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import Tool

def get_search_tool():
    # Create Tavily search tool
    tavily_tool = TavilySearchResults(
        name="Web Search",
        description="Search the web for current information",
        max_results=3  # Get top 3 results
    )
    
    return tavily_tool