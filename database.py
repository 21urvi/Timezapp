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
            self.cursor = self.db.cursor(dictionary=True)  # ✅ Returns dictionaries
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
        """Fetch all records from a query safely and return as a list of dictionaries."""
        if not self.db:
            print("Database connection not established.")
            return []
        try:
            with self.db.cursor(dictionary=True) as cursor:  # ✅ Returns data as dictionaries
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
            with self.db.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Fetch one error: {err}")
            return None

    def fetch_progress_data(self):
        """Fetch progress data by joining related task tables."""
        if not self.db:
            print("Database connection not established.")
            return []
        query = """
            SELECT p.progress_id, p.task_id, p.s_id, p.r_id, p.p_id, p.e_id, p.d_id,
                   t.task_name, t.date, t.priority, t.status,
                   pr.ptask_name, pr.p_date, pr.p_priority, pr.p_status,
                   r.rtask_name, r.rdate, r.rpriority, r.focus_point, r.rstatus,
                   s.subject, s.stask_name, s.sdate, s.spriority, s.sstatus,
                   e.etask_name, e.edate, e.epriority, e.estatus,
                   d.dtask_name, d.ddate, d.dpriority, d.dstatus
            FROM progress p
            LEFT JOIN tasks t ON p.task_id = t.task_id
            LEFT JOIN prectical pr ON p.p_id = pr.p_id
            LEFT JOIN revision r ON p.r_id = r.r_id
            LEFT JOIN subject s ON p.s_id = s.s_id
            LEFT JOIN exam e ON p.e_id = e.e_id
            LEFT JOIN discussion d ON p.d_id = d.d_id;
        """
        try:
            with self.db.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Fetch progress error: {err}")
            return []

    def close_connection(self):
        """Close the database connection properly."""
        if self.db:
            self.cursor.close()
            self.db.close()
