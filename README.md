```markdown
# 📊 NLP to SQL Query System

A natural language interface for querying Excel/CSV files using AI-powered SQL generation.

## Features

- 🗣️ Natural language to SQL conversion
- 📁 Support for CSV and Excel files
- 🤖 Powered by LangGraph and OpenAI GPT-4
- 📊 Interactive data visualization
- 🔍 Query history tracking
- 💡 Real-time data preview

## Installation

1. Clone the repository:
```bash
git clone https://github.com/krushna27/NLP-to-SQL-Query-System-LangGraph.git
cd nlp-to-sql-query-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

Run the Streamlit application:
```bash
streamlit run src/app.py
```

Then:
1. Upload your CSV or Excel file
2. Ask questions in natural language
3. View the AI-generated SQL and results

## Example Queries

- "What are the top 5 records?"
- "Show me the total count by category"
- "What is the average value?"
- "List all unique items"

## Architecture

The system uses LangGraph to create a multi-step workflow:
1. **Text-to-SQL**: Converts natural language to SQL
2. **Execute SQL**: Runs the query against the data
3. **Generate Answer**: Creates a natural language response

## Requirements

- OpenAI API key


```
