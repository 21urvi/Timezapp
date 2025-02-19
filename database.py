import mysql.connector

class DatabaseManager:
    def __init__(self):
        """Initialize the MySQL connection."""
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="urvi2115",
                database="timezap",
                autocommit=True  # Ensures automatic commit after queries
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            self.db = None

    def execute_query(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE queries with error handling."""
        if not self.db:
            print("Database connection not established.")
            return False
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, params or ())
                self.db.commit()
                return True
        except mysql.connector.Error as err:
            print(f"Query execution error: {err}")
            return False

    def fetch_all(self, query, params=None):
        """Fetch all records from a query safely."""
        if not self.db:
            print("Database connection not established.")
            return []
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Fetch error: {err}")
            return []

    def fetch_one(self, query, params=None):
        """Fetch a single record from a query safely."""
        if not self.db:
            print("Database connection not established.")
            return None
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Fetch one error: {err}")
            return None

    def close_connection(self):
        """Close the database connection properly."""
        if self.db:
            self.cursor.close()
            self.db.close()
