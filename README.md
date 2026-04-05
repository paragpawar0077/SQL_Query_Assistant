# 🎯 SQL Query Assistant

An AI-powered natural language to SQL query assistant built with Python, 
Google Gemini API, SQLite, and Streamlit.

## What it does
Ask questions in plain English and get answers from a real database — 
no SQL knowledge needed.

**Example:**
- "Which country has the most customers?" → runs SQL → "USA with 13 customers"
- "What are the top 5 genres by tracks?" → runs SQL → bar chart + answer

## Tech Stack
- **Python** — core language
- **Google Gemini API** — natural language to SQL conversion
- **SQLite** — database (Chinook music store dataset)
- **Streamlit** — web interface
- **Pandas** — data visualization

## Project Architecture

User Question (English)
↓
schema_extractor.py  → reads DB structure
↓
nl2sql.py            → Gemini converts question to SQL
↓
db_executor.py       → executes SQL on Chinook DB
↓
answer_generator.py  → Gemini explains results in English
↓
app.py               → Streamlit web interface

## 📁 Project Structure
sql-query-assistant/
├── app.py                  # Streamlit web interface
├── main.py                 # CLI version
├── schema_extractor.py     # Reads database structure
├── nl2sql.py               # Natural language → SQL (Gemini)
├── db_executor.py          # Executes SQL queries
├── answer_generator.py     # Results → Plain English (Gemini)
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not uploaded to GitHub)
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation

## Features
- Natural language to SQL conversion
- Syntax-highlighted SQL display
- Auto bar chart for numeric results
- Query history
- Error handling for invalid queries

## Setup

1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/sql-query-assistant
cd sql-query-assistant
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Download Chinook database
Download `Chinook_Sqlite.sqlite` from [here](https://github.com/lerocha/chinook-database) 
and rename it to `chinook.db`

4. Add your Gemini API key
Create a `.env` file:
GEMINI_API_KEY=your_key_here

5. Run the app
```bash
streamlit run app.py
```

---

## 🔍 How it works

1. **Schema Extraction** — automatically reads all tables and columns from the database and formats them for the AI prompt
2. **Prompt Engineering** — injects the schema into a carefully crafted Gemini prompt to ensure clean SQL output
3. **SQL Generation** — Gemini generates valid SQLite-compatible SQL from the user's question
4. **Safe Execution** — SQL runs on the real Chinook database with error handling
5. **Answer Generation** — Gemini explains the raw results in plain, human-readable English
6. **Auto Visualization** — automatically detects numeric results and renders a bar chart

---

## 🔧 Technical Highlights

- Designed a modular architecture with separation of concerns across 5 Python modules
- Applied prompt engineering techniques to control LLM output format
- Implemented session state management in Streamlit for query history
- Built automatic chart detection logic using pandas and Streamlit
- Used parameterized queries to prevent SQL injection attacks
- Secured API credentials using environment variables
