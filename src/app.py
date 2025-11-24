import streamlit as st
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
from agent.graph import create_sql_agent_graph
from database.loader import load_excel_to_sqlite

load_dotenv()

@st.cache_resource
def get_agent_graph():
    """Cache the agent graph"""
    return create_sql_agent_graph()

def query_excel_data(excel_path: str, user_query: str) -> dict:
    """Main function to process user queries against Excel data"""
    conn, schema = load_excel_to_sqlite(excel_path)
    conn.close()
    
    app = get_agent_graph()
    
    initial_state = {
        "messages": [],
        "user_query": user_query,
        "sql_query": "",
        "query_result": "",
        "final_answer": "",
        "excel_path": excel_path,
        "table_schema": schema
    }
    
    final_state = app.invoke(initial_state)
    
    return {
        "user_query": user_query,
        "sql_query": final_state["sql_query"],
        "query_result": final_state["query_result"],
        "final_answer": final_state["final_answer"]
    }

def main():
    st.set_page_config(
        page_title="NLP to SQL Query System",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Natural Language to SQL Query System")
    st.markdown("Ask questions about your data in plain English!")
    
    with st.sidebar:
        st.header("📁 Upload Data")
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your data file to query"
        )
        
        if uploaded_file is not None:
            file_path = f"temp_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ Loaded: {uploaded_file.name}")
            
            if st.checkbox("Show data preview"):
                try:
                    if file_path.endswith('.csv'):
                        df = pd.read_csv(file_path)
                    else:
                        df = pd.read_excel(file_path)
                    st.dataframe(df.head(10), use_container_width=True)
                    st.info(f"Total rows: {len(df)}")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
            
            if st.checkbox("Show table schema"):
                try:
                    conn, schema = load_excel_to_sqlite(file_path)
                    conn.close()
                    st.code(schema)
                except Exception as e:
                    st.error(f"Error loading schema: {e}")
    
    if uploaded_file is None:
        st.info("👈 Please upload a CSV or Excel file to get started")
        
        st.subheader("Example Queries")
        st.markdown("""
        Once you upload your data, you can ask questions like:
        - "What are the top 5 records?"
        - "Show me the total count by category"
        - "What is the average value?"
        - "List all unique items"
        """)
    else:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_query = st.text_input(
                "Ask a question about your data:",
                placeholder="e.g., What are the different payment methods and their counts?",
                key="query_input"
            )
        
        with col2:
            query_button = st.button("🔍 Search", type="primary", use_container_width=True)
        
        if query_button and user_query:
            with st.spinner("Processing your query..."):
                try:
                    result = query_excel_data(file_path, user_query)
                    
                    tab1, tab2, tab3 = st.tabs(["💬 Answer", "🔧 SQL Query", "📊 Raw Results"])
                    
                    with tab1:
                        st.markdown("### Answer")
                        st.success(result['final_answer'])
                    
                    with tab2:
                        st.markdown("### Generated SQL Query")
                        st.code(result['sql_query'], language='sql')
                    
                    with tab3:
                        st.markdown("### Query Results")
                        if "Error" in result['query_result']:
                            st.error(result['query_result'])
                        else:
                            st.text(result['query_result'])
                            
                            try:
                                if file_path.endswith('.csv'):
                                    df_temp = pd.read_csv(file_path)
                                else:
                                    df_temp = pd.read_excel(file_path)
                                conn = sqlite3.connect(':memory:')
                                df_temp.to_sql('data', conn, index=False, if_exists='replace')
                                df_result = pd.read_sql_query(result['sql_query'], conn)
                                conn.close()
                                
                                if not df_result.empty:
                                    st.dataframe(df_result, use_container_width=True)
                            except:
                                pass
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
        
        if query_button and user_query:
            st.session_state.query_history.append({
                'query': user_query,
                'answer': result['final_answer']
            })
        
        if st.session_state.query_history:
            with st.expander("📜 Query History"):
                for i, item in enumerate(reversed(st.session_state.query_history[-5:])):
                    st.markdown(f"**Q{len(st.session_state.query_history)-i}:** {item['query']}")
                    st.markdown(f"*A:* {item['answer']}")
                    st.divider()

if __name__ == "__main__":
    main()