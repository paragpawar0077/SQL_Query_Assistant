# SQL Query Assistant

An AI-powered natural language to SQL query assistant built with Python, Google Gemini API, SQLite, and Streamlit. Ask questions in plain English and get answers from a real database — no SQL knowledge needed.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Gemini API](https://img.shields.io/badge/Gemini-2.5--flash--lite-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![AWS EC2](https://img.shields.io/badge/AWS-EC2-FF9900)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What It Does

Type a question in plain English, and the app converts it to SQL, runs it against a live database, and returns a plain-English answer plus an auto-generated chart.

**Example queries:**

| Question | What Happens |
|---|---|
| "Which country has the most customers?" | Runs SQL → "USA with 13 customers" |
| "What are the top 5 genres by tracks?" | Runs SQL → bar chart + plain English answer |
| "Which artist has the most albums?" | Runs SQL → "Iron Maiden with 21 albums" |

---

## Architecture

```
User Question (Plain English)
        ↓
Schema Extraction — reads all tables and columns from SQLite DB
        ↓
NL → SQL (Gemini API) — converts question + schema into valid SQL
        ↓
SQL Execution — runs query on Chinook database
        ↓
Answer Generation (Gemini API) — explains raw results in plain English
        ↓
Streamlit UI — displays SQL, answer, and auto bar chart
```

---

## Project Structure

```
sql-query-assistant/
├── app.py                # Streamlit web interface
├── main.py               # CLI version
├── schema_extractor.py   # Reads and formats database schema for LLM prompt
├── nl2sql.py             # Natural language → SQL using Gemini
├── db_executor.py        # Executes SQL queries on SQLite
├── answer_generator.py   # Converts results → plain English using Gemini
├── chinook.db            # SQLite database (Chinook music store)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container build definition
├── .Dockerignore
├── .env                  # API keys (not committed to GitHub)
├── .gitignore
└── README.md
```

---

## Key Technical Decisions

### Prompt Engineering
The NL2SQL prompt injects the full database schema dynamically so the model always knows the exact table and column names. Key rules enforced in the prompt:
- Return SQL only — no markdown, no explanation
- For "top N" / "most" / "highest" queries — always include `COUNT` or `SUM` in `SELECT`
- Always use `GROUP BY` and `ORDER BY` for ranking questions

This prevents the most common LLM SQL failures (missing aggregations, wrong column names).

### Modular Architecture
Five separate modules with clear separation of concerns — schema extraction, SQL generation, execution, answer generation, and UI. Each module is independently testable via `if __name__ == "__main__"` blocks.

### Performance
`@st.cache_resource` caches the schema extractor, NL2SQL, executor, and answer generator on first load — prevents re-initialization on every user interaction in Streamlit.

### Session State
Query history is stored in `st.session_state` and displayed in reverse chronological order — persists across interactions within a session.

### Error Handling
API quota errors (429) are caught separately and shown with a user-friendly message rather than a raw traceback.

### Security
API credentials stored in a `.env` file and loaded via `python-dotenv`. `.env` is excluded from version control via `.gitignore`.

### Containerization & Deployment
The app is packaged as a Docker image (`Dockerfile` + `.Dockerignore`) and deployed on an AWS EC2 instance, running the container behind the instance's public IP/port.

---

## Database

**Chinook** — a sample music store SQLite database with 11 tables:

| Table | Description |
|---|---|
| Artist | Music artists |
| Album | Albums by artists |
| Track | Individual tracks |
| Genre | Music genres |
| Customer | Store customers |
| Invoice | Purchase records |
| InvoiceLine | Line items per invoice |
| Employee | Store employees |
| Playlist | User playlists |
| PlaylistTrack | Track-playlist mapping |
| MediaType | Audio format types |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Google Gemini API (`gemini-2.5-flash-lite`) | NL → SQL and answer generation |
| SQLite | Database engine |
| Streamlit | Web interface |
| Pandas | Chart rendering |
| python-dotenv | Environment variable management |
| Docker | Containerized deployment |
| AWS EC2 | Cloud hosting for the deployed container |

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/paragpawar0077/SQL_Query_Assistant
cd SQL_Query_Assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Gemini API key**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```
Get a free key at: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**4. Run the app**
```bash
streamlit run app.py
```

**Or run the CLI version:**
```bash
python main.py
```

**Or run with Docker (locally):**
```bash
docker build -t sql-query-assistant .
docker run -p 8501:8501 --env-file .env sql-query-assistant
```

---

## Deployment (AWS EC2)

The app is containerized and deployed on an AWS EC2 instance:

```bash
# On the EC2 instance
git clone https://github.com/paragpawar0077/SQL_Query_Assistant
cd SQL_Query_Assistant

# Build the image
docker build -t sql-query-assistant .

# Run the container (mount your .env with the Gemini API key)
docker run -d -p 8501:8501 --env-file .env --restart unless-stopped sql-query-assistant
```

Make sure the EC2 security group allows inbound traffic on port `8501` (or whichever port you expose) so the Streamlit app is reachable from the browser.

---

## Features

- Natural language to SQL conversion using Gemini
- Dynamic schema injection into LLM prompt
- Syntax-highlighted SQL display
- Auto bar chart for numeric (label, value) results
- Query history within session
- Separate error handling for API quota limits
- Modular architecture — each component independently testable
- Docker support for containerized deployment
- Deployed and running on AWS EC2

---

## Known Limitations

- Currently supports SQLite only — no PostgreSQL or MySQL support
- Schema is read once on startup — requires restart if database changes
- No query caching — identical questions re-call the Gemini API each time

---

## Author

**Parag Pawar**
- GitHub: [@paragpawar0077](https://github.com/paragpawar0077)
- Email: paragpawar0077@gmail.com