# 🤖 AI Agentic Workflow Executor

This is a **Streamlit web app** that demonstrates an agentic workflow powered by multiple intelligent agents using [LangGraph](https://github.com/langchain-ai/langgraph). It decomposes a user query into smaller tasks, executes them using tools like web search and calculator, reflects on intermediate results, and handles errors — all step-by-step in an interactive UI.

---

## 🚀 Features

- ✅ Natural Language Task Planning
- 🛠️ Tool Execution (Search, Calculator)
- 🔁 Reflection and Improvement
- ⚠️ Error Detection & Handling
- 🎯 Final Output Summary
- 🌐 Powered by LangGraph and LangChain agents

---

## 🧠 Architecture

This project includes:
- **PlanAgent**: Breaks the query into tasks.
- **ToolAgent**: Executes each task using tools (search, calculator).
- **ReflectionAgent**: Reflects on the task results and adjusts the workflow.
- **LangGraph StateGraph**: Manages task flow and transitions.
- **Streamlit App**: UI for user input and displaying results step-by-step.

---

## 🧰 Requirements

- Python 3.8+
- [LangGraph](https://pypi.org/project/langgraph/)
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Install dependencies:
```bash
pip install -r requirements.txt

Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here


Run the App
bash
Copy
Edit
streamlit run app.py
Make sure the following files are present:

graph.py – defines the workflow graph and nodes.

state.py – contains the WorkflowState dataclass.

agents/ – contains PlanAgent, ToolAgent, ReflectionAgent.

tools.py – defines the tools used in ToolAgent.

Example Workflow
User Input: "What's the population of India? What is 10% of it?"

Planning Node: Breaks it into two sub-tasks.

Execution Node: Executes each task with a tool.

Reflection Node: Thinks if the result makes sense.

Final Result: Displays the results in a friendly format.



📄 License
This project is for educational and demonstration purposes. Feel free to modify and extend it.


Made  by https://github.com/Yas5584
