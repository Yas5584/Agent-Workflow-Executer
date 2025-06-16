import os
import streamlit as st
from dotenv import load_dotenv
from graph import build_workflow
from state import WorkflowState

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# Page config
st.set_page_config(page_title="AI Agent Workflow", page_icon="🤖", layout="centered")
st.title("🔄 Agentic Workflow Executor")

# Input from user
query = st.text_input("Enter your query:")

def run_workflow(user_query: str):
    # Initialize workflow
    app = build_workflow()

    # Initial state
    state = WorkflowState(
        input=user_query,
        tasks=[],
        current_task=None,
        results={},
        reflection=None,
        should_continue=True,
        error=None
    )

    final_state = None

    with st.spinner("Running agentic workflow..."):
        for step in app.stream(state):
            for node, node_state in step.items():
                with st.expander(f"🔹 {node.upper()} NODE", expanded=False):
                    if node == "plan":
                        st.write("**Tasks Planned:**", node_state.get("tasks", []))

                    if node == "execute":
                        task = node_state.get("current_task", "N/A")
                        result = node_state.get("results", {}).get(task, "No result available")
                        st.write(f"**Executed Task:** `{task}`")
                        st.write("**Result:**", result)

                    if node == "reflect":
                        st.write("**Reflection:**", node_state.get("reflection", "No reflection"))

                    if node == "handle_error":
                        st.error(f"**Error:** {node_state.get('error', 'No error')}")

            final_state = list(step.values())[0]  # Save last state

    return final_state

# Run workflow on button click
if query:
    final_state = run_workflow(query)

    # Display Final Results
    if final_state:
        st.subheader("✅ Final Results")
        for task, result in final_state.get("results", {}).items():
            st.markdown(f"**• {task}**: {result}")
