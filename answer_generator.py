from google import genai
from dotenv import load_dotenv
import os

class AnswerGenerator:
    """
    Uses Gemini to convert SQL query results into human-readable explanations.
    """

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.client = genai.Client(api_key=api_key)

    def generate_answer(self, question, sql, results):
        """
        Generate a natural language explanation of SQL query results.
        """

        prompt = f"""
You are a data analyst.

User Question:
{question}

SQL Query:
{sql}

Query Results:
{results}

Explain the results clearly in plain English.
- Be concise
- Directly answer the question
- Mention key values from the result
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

            return response.text.strip()

        except Exception as e:
            return f"Error generating answer: {str(e)}"


# Quick test
if __name__ == "__main__":
    generator = AnswerGenerator()

    question = "Which artist has the most albums?"
    sql = """SELECT Artist.Name, COUNT(*)
             FROM Album
             JOIN Artist ON Album.ArtistId = Artist.ArtistId
             GROUP BY Artist.ArtistId
             ORDER BY COUNT(*) DESC
             LIMIT 1"""

    results = [("Iron Maiden", 21)]

    answer = generator.generate_answer(question, sql, results)
    print(answer)
