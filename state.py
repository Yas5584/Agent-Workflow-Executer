from typing import TypedDict, List, Dict, Any, Optional

class WorkflowState(TypedDict):
    """Represents the state of our agentic workflow"""
    input: str
    tasks: List[str]
    current_task: Optional[str]
    results: Dict[str, str]
    reflection: Optional[str]
    should_continue: bool
    error: Optional[str]