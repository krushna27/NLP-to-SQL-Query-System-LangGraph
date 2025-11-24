from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import text_to_sql_node, execute_sql_node, generate_answer_node

def create_sql_agent_graph():
    """Create the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("text_to_sql", text_to_sql_node)
    workflow.add_node("execute_sql", execute_sql_node)
    workflow.add_node("generate_answer", generate_answer_node)
    
    # Add edges
    workflow.set_entry_point("text_to_sql")
    workflow.add_edge("text_to_sql", "execute_sql")
    workflow.add_edge("execute_sql", "generate_answer")
    workflow.add_edge("generate_answer", END)
    
    return workflow.compile()