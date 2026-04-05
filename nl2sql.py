from google import genai
from dotenv import load_dotenv
import os

class NL2SQL:

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def generate_sql(self, question, schema):
        prompt = f"""
You are a SQL expert. Given the database schema below, convert the user question into a valid SQL query.

Schema:
{schema}

Question: {question}

Rules:
- Return ONLY the SQL query
- No explanation
- No markdown backticks
- No extra text
- When asked for "top N", "most", "highest", "lowest" — ALWAYS include the COUNT or SUM value in SELECT
- Always include GROUP BY and ORDER BY for ranking questions
- Example: "top 5 genres by tracks" → SELECT Genre.Name, COUNT(Track.TrackId) AS TrackCount FROM ...

"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text.strip()



if __name__ == "__main__":
    from schema_extractor import SchemaExtractor

    # Load database schema dynamically to ensure query accuracy
    extractor = SchemaExtractor("chinook.db")
    schema = extractor.get_schema()

    # Initialize NL → SQL converter using Gemini
    nl2sql = NL2SQL()
    # Sample test queries to validate SQL generation
    questions = [
        "Show me all customers from Brazil",
        "Which artist has the most albums?",
        "What are the top 5 most expensive tracks?"
    ]
    # Generate SQL queries for each input question
    for question in questions:
        print(f"Question: {question}")
        sql = nl2sql.generate_sql(question, schema)
        print(f"SQL: {sql}")
        print()
