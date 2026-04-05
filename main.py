from schema_extractor import SchemaExtractor
from nl2sql import NL2SQL
from db_executor import DBExecutor
from answer_generator import AnswerGenerator


def main():
    """
    CLI interface for the SQL Query Assistant.
    Converts natural language → SQL → execution → explanation.
    """

    # Initialize components
    extractor = SchemaExtractor("chinook.db")
    nl2sql = NL2SQL()
    executor = DBExecutor("chinook.db")
    generator = AnswerGenerator()

    # Load schema once (optimization)
    schema = extractor.get_schema()

    print("🎯 SQL Query Assistant")
    print("Type 'exit' to quit\n")

    while True:
        try:
            question = input("Ask a question: ").strip()

            if not question:
                print("⚠️ Please enter a valid question.\n")
                continue

            if question.lower() == "exit":
                print("Goodbye!")
                break

            # Step 1: NL → SQL
            sql = nl2sql.generate_sql(question, schema)
            print(f"\n🧠 Generated SQL:\n{sql}")

            # Step 2: Execute query
            results = executor.run_query(sql)
            print(f"\n📊 Raw Results:\n{results}")

            # Step 3: Generate answer
            answer = generator.generate_answer(question, sql, results)
            print(f"\n✅ Final Answer:\n{answer}\n")

        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()
