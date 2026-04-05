import sqlite3
class DBExecutor:
    def __init__(self, db_path):
        self.db_path = db_path

    def run_query(self, query):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return str(e)
        finally:
            conn.close()

# Test it
if __name__ == "__main__":
    executor = DBExecutor("chinook.db")
    query = "SELECT Name FROM Artist LIMIT 5;"
    results = executor.run_query(query)
    print(results)