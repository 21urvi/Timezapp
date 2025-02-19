from flask import render_template, session, redirect, url_for, jsonify
from database import DatabaseManager

class CalendarManager:
    def __init__(self):
        self.db = DatabaseManager()

    def show_calendar(self):
        """Fetch all tasks and return them as JSON for FullCalendar.js"""
        if "user" not in session:
            return redirect(url_for("login"))

        # Fetching all tasks from different tables
        tasks = self.db.fetch_all("SELECT task_id, task_name, date FROM tasks")
        subjects = self.db.fetch_all("SELECT s_id, sname, s_date FROM subject")
        revisions = self.db.fetch_all("SELECT r_id, rtask_name, r_date FROM revision")
        practicals = self.db.fetch_all("SELECT p_id, ptask_name, p_date FROM practical")
        exams = self.db.fetch_all("SELECT e_id, ename, edate FROM exam")
        discussions = self.db.fetch_all("SELECT d_id, dtask_name, ddate FROM discussion")

        # Convert tuples to JSON format for FullCalendar.js
        events = []
        for task in tasks:
            events.append({"id": f"T{task[0]}", "title": f"Task: {task[1]}", "start": task[2], "color": "#007bff"})
        for subject in subjects:
            events.append({"id": f"S{subject[0]}", "title": f"Subject: {subject[1]}", "start": subject[2], "color": "#28a745"})
        for revision in revisions:
            events.append({"id": f"R{revision[0]}", "title": f"Revision: {revision[1]}", "start": revision[2], "color": "#ffc107"})
        for practical in practicals:
            events.append({"id": f"P{practical[0]}", "title": f"Practical: {practical[1]}", "start": practical[2], "color": "#17a2b8"})
        for exam in exams:
            events.append({"id": f"E{exam[0]}", "title": f"Exam: {exam[1]}", "start": exam[2], "color": "#dc3545"})
        for discussion in discussions:
            events.append({"id": f"D{discussion[0]}", "title": f"Discussion: {discussion[1]}", "start": discussion[2], "color": "#6f42c1"})

        return render_template("calendar.html", events=events)
