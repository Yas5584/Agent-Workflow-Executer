from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from typing import List
import os
from dotenv import load_dotenv
load_dotenv()




class PlanAgent:
    def __init__(self, model: str = "llama-3.3-70b-versatile",api_key:str=os.getenv("GROQ_API_KEY")):
        self.llm = ChatGroq(model=model,groq_api_key=api_key)
    
    def generate_tasks(self, user_input: str) -> List[str]:
        """Break down a complex query into actionable tasks"""
        prompt = f"""
        You are an expert planner. Break this complex task into clear, 
        actionable sub-tasks. Return ONLY a numbered list:
        
        Task: {user_input}
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return self._parse_tasks(response.content)
    
    def _parse_tasks(self, response: str) -> List[str]:
        """Extract tasks from the LLM response"""
        tasks = []
        for line in response.split("\n"):
            if line.strip() and any(char.isdigit() for char in line[:3]):
                task = line.split(".", 1)[-1].strip()
                tasks.append(task)
        return tasks