import sqlite3

class SchemaExtractor:
    """
    Extracts database schema (tables + columns) from a SQLite database.
    Output is formatted as a string to provide context to the LLM for SQL generation.
    """

    def __init__(self, db_path):
        self.db_path = db_path

    def get_schema(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Fetch all table names from SQLite system metadata
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        schema = ""

        for table in tables:
            table_name = table[0]
            schema += f"Table: {table_name}\n"

            # Get column details (name + datatype) for each table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            for col in columns:
                schema += f"  - {col[1]} ({col[2]})\n"

            schema += "\n"

        connection.close()
        return schema


# Quick local test to verify schema extraction
if __name__ == "__main__":
    extractor = SchemaExtractor("chinook.db")
    schema = extractor.get_schema()
    print(schema)
