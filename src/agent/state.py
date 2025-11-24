from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    """State structure for the SQL agent workflow"""
    messages: Annotated[list, operator.add]
    user_query: str
    sql_query: str
    query_result: str
    final_answer: str
    excel_path: str
    table_schema: str