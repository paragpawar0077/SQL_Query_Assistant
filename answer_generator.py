from google import genai
from dotenv import load_dotenv
import os

class AnswerGenerator:

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) 

    def generate_answer(self, question, sql, results):


        prompt = f"""
        Question: {question}
        SQL: {sql}
        Results: {results}
        Please explain the results in plain English, and how they answer the question.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return response.text.strip()



# Test it
if __name__ == "__main__":
    generator = AnswerGenerator()

    question = "Which artist has the most albums?"
    sql = "SELECT Artist.Name, COUNT(*) FROM Album JOIN Artist ON Album.ArtistId = Artist.ArtistId GROUP BY Artist.ArtistId ORDER BY COUNT(*) DESC LIMIT 1"
    results = [("Iron Maiden", 21)]

    answer = generator.generate_answer(question, sql, results)
    print(answer)