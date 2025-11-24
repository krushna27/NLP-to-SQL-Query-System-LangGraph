from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
import pandas as pd
from .state import AgentState
import os
import sys
# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.state import AgentState
from database.loader import load_excel_to_sqlite

def get_llm():
    """Initialize and return LLM instance"""
    return ChatOpenAI(model="gpt-4o")

def text_to_sql_node(state: AgentState) -> AgentState:
    """Convert user query to SQL using LLM"""
    llm = get_llm()
    
    system_prompt = f"""You are a SQL expert. Convert the user's natural language query into a valid SQLite query.

Database Schema:
{state['table_schema']}

Rules:
- Generate ONLY the SQL query, no explanations
- Use proper SQLite syntax
- The table name is 'data'
- Return only SELECT statements
- Be precise and handle edge cases
- Do not include markdown formatting or code blocks"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Convert this to SQL: {state['user_query']}")
    ]
    
    response = llm.invoke(messages)
    sql_query = response.content.strip()
    
    # Clean up any markdown formatting
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return {
        "sql_query": sql_query,
        "messages": [AIMessage(content=f"Generated SQL: {sql_query}")]
    }

def execute_sql_node(state: AgentState) -> AgentState:
    """Execute the SQL query and return results"""
    try:
        conn, _ = load_excel_to_sqlite(state['excel_path'])
        df_result = pd.read_sql_query(state['sql_query'], conn)
        conn.close()
        
        if df_result.empty:
            query_result = "No results found."
        else:
            query_result = df_result.to_string(index=False)
        
        return {
            "query_result": query_result,
            "messages": [AIMessage(content=f"Query executed successfully. Rows returned: {len(df_result)}")]
        }
    except Exception as e:
        error_msg = f"Error executing query: {str(e)}"
        return {
            "query_result": error_msg,
            "messages": [AIMessage(content=error_msg)]
        }

def generate_answer_node(state: AgentState) -> AgentState:
    """Generate natural language answer from query results"""
    llm = get_llm()
    
    system_prompt = """You are a helpful assistant that explains query results in natural language.
    
Your task:
- Analyze the query results provided
- Generate a clear, concise, and natural language response
- If there are numbers, present them in a readable format
- If there are multiple rows, summarize appropriately
- Remove markdown formatting if present
- Be conversational and helpful"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
User's original question: {state['user_query']}

SQL Query executed: {state['sql_query']}

Query Results:
{state['query_result']}

Please provide a natural language answer to the user's question based on these results.""")
    ]
    
    response = llm.invoke(messages)
    final_answer = response.content.strip()
    
    return {
        "final_answer": final_answer,
        "messages": [AIMessage(content=final_answer)]
    }