import sqlite3

class DBExecutor:
    """
    Executes SQL queries on a SQLite database.
    Returns query results or raises meaningful errors.
    """

    def __init__(self, db_path):
        self.db_path = db_path

    def run_query(self, query):
        """Execute a SQL query and return results."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results

        except sqlite3.Error as e:
            # Return database-specific errors for better debugging
            return f"Database error: {str(e)}"

        finally:
            conn.close()


# Quick test
if __name__ == "__main__":
    executor = DBExecutor("chinook.db")
    query = "SELECT Name FROM Artist LIMIT 5;"
    results = executor.run_query(query)
    print(results)
