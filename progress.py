from flask import render_template, session, redirect, url_for
from database import DatabaseManager

class ProgressManager:
    def __init__(self):
        self.db = DatabaseManager()

    def show_progress(self):
        """Show progress for tasks and practicals"""
        if "user" not in session:
            return redirect(url_for("login"))

        completed_tasks = self.db.fetch_all("SELECT COUNT(*) FROM tasks WHERE status = 'Complete'")
        total_tasks = self.db.fetch_all("SELECT COUNT(*) FROM tasks")

        completed_practicals = self.db.fetch_all("SELECT COUNT(*) FROM practical WHERE p_status = 'Complete'")
        total_practicals = self.db.fetch_all("SELECT COUNT(*) FROM practical")

        progress_data = {
            "completed_tasks": completed_tasks[0][0],
            "total_tasks": total_tasks[0][0],
            "completed_practicals": completed_practicals[0][0],
            "total_practicals": total_practicals[0][0]
        }

        return render_template("progress.html", progress=progress_data)
