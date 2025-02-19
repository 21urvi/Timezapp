from flask import session, render_template, redirect, url_for, jsonify
from database import DatabaseManager


class TaskManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_tasks(self):
        """Fetch all tasks"""
        if 'user' not in session:
            return redirect(url_for('login'))
        tasks = self.db.fetch_all("SELECT * FROM tasks")
        return render_template("tasks.html", tasks=tasks)

    def add_task(self, request):
        """Add a new task"""
        if 'user' not in session:
            return redirect(url_for('login'))

        data = request.form
        self.db.execute_query("INSERT INTO tasks (task_name, date, priority, status) VALUES (%s, %s, %s, 'Incomplete')",
                              (data["task_name"], data["date"], data["priority"]))
        return redirect(url_for("home"))

    def delete_task(self, task_id):
        """Delete a task"""
        if 'user' not in session:
            return jsonify(success=False, message="Unauthorized"), 403

        self.db.execute_query("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        return jsonify(success=True)
