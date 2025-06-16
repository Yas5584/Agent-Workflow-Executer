from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_groq import ChatGroq

from typing import List
import os
from dotenv import load_dotenv
load_dotenv()

class ToolAgent:
    def __init__(self, tools: list, model: str = "llama-3.1-8b-instant",api_key:str=os.getenv("GROQ_API_KEY")):
        self.tools = tools
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Use tools to solve tasks."),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad", optional=True)
        ])
        self.agent = create_tool_calling_agent(
            ChatGroq(model=model,groq_api_key=api_key), 
            tools, 
            prompt
        )
        self.executor = AgentExecutor(
            agent=self.agent, 
            tools=tools, 
            handle_parsing_errors=True,
            verbose=True
        )
    
    def execute_task(self, task: str) -> str:
        """Execute a single task using available tools"""
        try:
            result = self.executor.invoke({"input": task})
            return result["output"]
        except Exception as e:
            return f"Error: {str(e)}"