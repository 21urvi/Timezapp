from flask import session, render_template, redirect, url_for, jsonify, request
from database import DatabaseManager

class DiscussionManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_discussions(self):
        """Fetch all discussions"""
        if 'user' not in session:
            return redirect(url_for('login'))

        discussions = self.db.fetch_all("""
            SELECT d.d_id, d.dtask_name, t.task_name AS related_task, d.ddate, d.dpriority, d.dstatus
            FROM discussion d
            JOIN tasks t ON d.task_id = t.task_id
        """)
        tasks = self.db.fetch_all("SELECT task_id, task_name FROM tasks")  # Fetch tasks for dropdown
        return render_template("discussion.html", discussions=discussions, tasks=tasks)

    def add_discussion(self):
        """Add a new discussion"""
        if 'user' not in session:
            return redirect(url_for('login'))

        data = request.form
        print("Received Form Data:", data)  # Debugging

        dtask_name = data.get("dtask_name")
        task_id = data.get("task_id")
        ddate = data.get("ddate")
        dpriority = data.get("dpriority")

        if not all([dtask_name, task_id, ddate, dpriority]):
            return jsonify(success=False, message="Missing required fields"), 400  # Handle missing fields

        self.db.execute_query("""
            INSERT INTO discussion (dtask_name, task_id, ddate, dpriority, dstatus)
            VALUES (%s, %s, %s, %s, 'Pending')
        """, (dtask_name, task_id, ddate, dpriority))

        return redirect(url_for("discussion"))

    def delete_discussion(self, d_id):
        """Delete a discussion"""
        if 'user' not in session:
            return jsonify(success=False, message="Unauthorized"), 403

        self.db.execute_query("DELETE FROM discussion WHERE d_id = %s", (d_id,))
        return jsonify(success=True)
