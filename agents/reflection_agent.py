from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')


class ReflectionAgent:
    def __init__(self, model: str = "llama-3.1-8b-instant",api_key:str=os.getenv("GROQ_API_KEY")):
        self.llm = ChatGroq(model=model,groq_api_key=api_key)
    
    def reflect(self, state: dict) -> dict:
        """Analyze progress and suggest improvements"""
        prompt = [
            SystemMessage(content="You are a reflection agent. Review progress and suggest improvements."),
            HumanMessage(content=self._build_prompt(state))
        ]
        response = self.llm.invoke(prompt)
        return self._parse_response(response.content)
    
    def _build_prompt(self, state: dict) -> str:
        return f"""
        Original Task: {state['input']}
        Completed Tasks: {len(state['results'])}/{len(state['tasks']) + len(state['results'])}
        Results: {state['results']}
        
        Suggestions needed:
        - Should we add, remove, or modify any tasks?
        - Are there any errors to address?
        - Should we continue processing?
        """
    
    def _parse_response(self, response: str) -> dict:
        # Simplified parsing - in real implementation you'd extract structured data
        return {"reflection": response}