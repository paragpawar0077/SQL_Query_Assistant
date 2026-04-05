from schema_extractor import SchemaExtractor
from nl2sql import NL2SQL
from db_executor import DBExecutor
from answer_generator import AnswerGenerator


def main():
    
    extractor = SchemaExtractor("chinook.db")
    nl2sql = NL2SQL()
    executor = DBExecutor("chinook.db")
    generator = AnswerGenerator()

    
    schema = extractor.get_schema()

    print("🎯 SQL Query Assistant")
    print("Type 'exit' to quit\n")

    
    while True:

        
        question = input("Ask a question: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        
        sql = nl2sql.generate_sql(question, schema)
        
        
        print(f"Generated SQL: {sql}")
        
        results = executor.run_query(sql)
        
        print(f"Raw Results: {results}")
        
        answer = generator.generate_answer(question, sql, results)
        
        print(f"Final Answer: {answer}")
        print()

if __name__ == "__main__":
    main()