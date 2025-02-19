from flask import render_template, session, redirect, url_for
from database import DatabaseManager

class CalendarManager:
    def __init__(self):
        self.db = DatabaseManager()

    def show_calendar(self):
        """Show calendar with tasks and practicals"""
        if "user" not in session:
            return redirect(url_for("login"))

        tasks = self.db.fetch_all("SELECT task_name, date FROM tasks")
        practicals = self.db.fetch_all("SELECT ptask_name, p_date FROM practical")

        return render_template("calendar.html", tasks=tasks, practicals=practicals)
