from flask import session, redirect, url_for, jsonify
from database import DatabaseManager

class CalendarManager:
    def __init__(self):
        self.db = DatabaseManager()

    def fetch_tasks(self):
        """Fetch all tasks from different tables and return them as JSON for FullCalendar.js."""
        if "user" not in session:
            return redirect(url_for("login"))

        tasks = self.db.fetch_all("SELECT task_id, task_name, DATE_FORMAT(date, '%Y-%m-%d') as date FROM tasks")
        subjects = self.db.fetch_all("SELECT s_id, stask_name, DATE_FORMAT(sdate, '%Y-%m-%d') as date FROM subject")
        revisions = self.db.fetch_all("SELECT r_id, rtask_name, DATE_FORMAT(rdate, '%Y-%m-%d') as date FROM revision")
        practicals = self.db.fetch_all("SELECT p_id, ptask_name, DATE_FORMAT(p_date, '%Y-%m-%d') as date FROM practical")
        exams = self.db.fetch_all("SELECT e_id, etask_name, DATE_FORMAT(edate, '%Y-%m-%d') as date FROM exam")
        discussions = self.db.fetch_all("SELECT d_id, dtask_name, DATE_FORMAT(ddate, '%Y-%m-%d') as date FROM discussion")

        events = []

        def add_events(data, title_prefix, color):
            for row in data:
                events.append({
                    "title": f"{title_prefix}: {row[list(row.keys())[1]]}",
                    "start": row['date'],
                    "color": color
                })

        add_events(tasks, "Task", "#007bff")  # Blue
        add_events(subjects, "Subject", "#28a745")  # Green
        add_events(revisions, "Revision", "#ffc107")  # Yellow
        add_events(practicals, "Practical", "#17a2b8")  # Cyan
        add_events(exams, "Exam", "#dc3545")  # Red
        add_events(discussions, "Discussion", "#6f42c1")  # Purple

        return jsonify(events)
