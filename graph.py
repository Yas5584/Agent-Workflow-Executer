from langgraph.graph import StateGraph, END
from agents.plan_agent import PlanAgent
from agents.tool_agent import ToolAgent
from agents.reflection_agent import ReflectionAgent
from tools import get_search_tool, get_calculator_tool
from state import WorkflowState
from IPython.display import Image,display

def build_workflow():
    # Initialize agents and tools
    plan_agent = PlanAgent()
    tool_agent = ToolAgent(tools=[get_search_tool(), get_calculator_tool()])
    reflection_agent = ReflectionAgent()
    
    # Define workflow graph
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("plan", plan_node)
    workflow.add_node("execute", execute_node)
    workflow.add_node("reflect", reflect_node)
    workflow.add_node("handle_error", handle_error_node)
    
    # Set entry point
    workflow.set_entry_point("plan")
    
    # Define edges
    workflow.add_edge("plan", "execute")
    workflow.add_conditional_edges(
        "execute",
        decide_next_step,
        {
            "continue": "reflect",
            "error": "handle_error",
            "complete": END
        }
    )
    workflow.add_edge("reflect", "execute")
    workflow.add_edge("handle_error", "reflect")
  
   
    

    
    return workflow.compile()

# Node implementations
def plan_node(state: WorkflowState) -> dict:
    plan_agent = PlanAgent()
    tasks = plan_agent.generate_tasks(state["input"])
    return {
        "tasks": tasks, 
        "should_continue": True,
        "results": state.get("results", {}),
        "reflection": state.get("reflection", None),
        "error": state.get("error", None)
    }

def execute_node(state: WorkflowState) -> dict:
    if not state["tasks"]:
        return {
            "should_continue": False,
            "tasks": [],
            "results": state.get("results", {}),
            "reflection": state.get("reflection", None),
            "error": state.get("error", None)
        }
    
    tool_agent = ToolAgent(tools=[get_search_tool(), get_calculator_tool()])
    current_task = state["tasks"].pop(0)
    result = tool_agent.execute_task(current_task)
    
    # Update results
    new_results = state.get("results", {}).copy()
    new_results[current_task] = result
    
    return {
        "current_task": current_task,
        "tasks": state["tasks"],  # Return updated task list
        "results": new_results,
        "error": None if "Error:" not in result else result,
        "should_continue": True,
        "reflection": state.get("reflection", None)
    }

def reflect_node(state: WorkflowState) -> dict:
    reflection_agent = ReflectionAgent()
    reflection = reflection_agent.reflect(state)
    return {
        "reflection": reflection["reflection"], 
        "should_continue": True,
        "tasks": state.get("tasks", []),
        "results": state.get("results", {}),
        "error": state.get("error", None)
    }

def handle_error_node(state: WorkflowState) -> dict:
    return {
        "error": None, 
        "should_continue": True,
        "tasks": state.get("tasks", []),
        "results": state.get("results", {}),
        "reflection": state.get("reflection", None)
    }

# Decision logic
def decide_next_step(state: WorkflowState) -> str:
    if state.get("error"):
        return "error"
    if not state.get("tasks", []):
        return "complete"
    return "continue"