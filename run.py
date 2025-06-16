from graph import build_workflow
from state import WorkflowState
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

def run_workflow(user_query: str):
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
    
    # Initializing  workflow
    app = build_workflow()
    print(app.get_graph().draw_mermaid())
    app.get_graph().print_ascii()
    # Set initial state
    state = WorkflowState(
        input=user_query,
        tasks=[],
        current_task=None,
        results={},
        reflection=None,
        should_continue=True,
        error=None
    )
    
    # Execute workflow and capture final state
    final_state = None
    for step in app.stream(state):
        for node, node_state in step.items():
            print(f"--- {node.upper()} NODE ---")
            print(f"Tasks: {node_state.get('tasks', [])}")
            
            if node == "execute":
                current_task = node_state.get('current_task', 'N/A')
                print(f"Executed: {current_task}")
                
                # Get result safely
                results = node_state.get('results', {})
                result = results.get(current_task, "No result available")
                print(f"Result: {result}")
                
            if node == "reflect":
                print(f"Reflection: {node_state.get('reflection', 'No reflection')}")
            
            if node == "handle_error":
                print(f"Handled error: {node_state.get('error', 'No error')}")
            
            print()
        
        # Capture the final state from the last step
        final_state = list(step.values())[0]
    
    return final_state

if __name__ == "__main__":
    
    query = "What's the current population of India? What would be 15% of that population?"
    final_state = run_workflow(query)
    
    
    print("\nFINAL RESULTS:")

    for task, result in final_state.get("results", {}).items():
        print(f"• {task}: {result}")