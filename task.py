from flask import Flask, session, render_template, redirect, url_for, request, jsonify
from database import DatabaseManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security

db = DatabaseManager()

class TaskManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_tasks(self):
        """Fetch all tasks"""
        if "user" in session:
            tasks = self.db.fetch_all("SELECT * FROM tasks")
            return render_template("tasks.html", tasks=tasks)
        return redirect(url_for("login"))

    def get_tasks_json(self):
        """Fetch tasks as JSON"""
        if "user" in session:
            tasks = self.db.fetch_all("SELECT task_id, task_name, date FROM tasks")
            return jsonify([
                {"id": task["task_id"], "title": task["task_name"], "start": task["date"].strftime('%Y-%m-%d'), "color": "#007bff"}
                for task in tasks
            ])
        return jsonify({"error": "Unauthorized"}), 403

    def add_task(self):
        """Add a new task dynamically"""
        if "user" in session:
            try:
                data = request.form
                insert_query = """
                    INSERT INTO tasks (task_name, date, priority, status) 
                    VALUES (%s, %s, %s, 'Pending')
                """
                if self.db.execute_query(insert_query, (data["task_name"], data["date"], data.get("priority", "Medium"))):
                    last_task = self.db.fetch_one("SELECT LAST_INSERT_ID() as task_id")
                    if last_task:
                        task_id = last_task["task_id"]
                        self.db.execute_query("INSERT INTO progress (task_id) VALUES (%s)", (task_id,))
                    return jsonify(success=True, message="Task added successfully!")
            except Exception as e:
                return jsonify(success=False, message="Error adding task!", error=str(e))
        return jsonify(success=False, message="Unauthorized")

    def delete_task(self, task_id):
        """Delete a task dynamically"""
        if "user" in session:
            try:
                task = self.db.fetch_one("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
                if not task:
                    return jsonify(success=False, message="Task not found!")
                self.db.execute_query("DELETE FROM progress WHERE task_id = %s", (task_id,))
                self.db.execute_query("DELETE FROM tasks WHERE task_id = %s", (task_id,))
                return jsonify(success=True, message="Task deleted successfully!")
            except Exception as e:
                return jsonify(success=False, message="Error deleting task!", error=str(e))
        return jsonify(success=False, message="Unauthorized")
