from flask import session, render_template, redirect, url_for, jsonify
from database import DatabaseManager

class PracticalTaskManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_practical_tasks(self):
        """Fetch all practical tasks"""
        if "user" in session:
            practicals = self.db.fetch_all("SELECT * FROM practical")
            return render_template("practical.html", practicals=practicals)
        return redirect(url_for("login"))

    def add_practical_task(self, request):
        """Add a new practical task"""
        if "user" in session:
            data = request.form
            self.db.execute_query(
                "INSERT INTO practical (ptask_name, p_date, p_priority, p_status) VALUES (%s, %s, %s, 'Incomplete')",
                (data["task_name"], data["date"], data["priority"]))
            return redirect(url_for("practical"))
        return redirect(url_for("login"))

    def delete_practical_task(self, p_id):
        """Delete a practical task"""
        if "user" in session:
            self.db.execute_query("DELETE FROM practical WHERE p_id = %s", (p_id,))
            return jsonify(success=True)
        return jsonify(success=False, message="Unauthorized")
