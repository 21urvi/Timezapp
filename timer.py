from flask import session, render_template, redirect, url_for
from database import DatabaseManager

class TimerManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_task_timer(self, task_id):
        """Fetch task details for the timer"""
        if 'user' not in session:
            return redirect(url_for('login'))

        task = self.db.fetch_one("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        if task:
            return render_template("timer.html", task=task)
        return redirect(url_for("home"))

    def get_practical_timer(self, p_id):
        """Fetch practical task details for the timer"""
        if "user" not in session:
            return redirect(url_for("login"))

        practical = self.db.fetch_one("SELECT * FROM practical WHERE p_id = %s", (p_id,))
        if practical:
            return render_template("timer.html", practical=practical)
        return redirect(url_for("practical"))

    def get_subject_timer(self, s_id):
        """Fetch subject task details for the timer"""
        if "user" not in session:
            return redirect(url_for("login"))

        subject = self.db.fetch_one("SELECT * FROM subject WHERE s_id = %s", (s_id,))
        if subject:
            return render_template("subject_timer.html", subject=subject)
        return redirect(url_for("subject"))

    def get_exam_timer(self, e_id):
        """Fetch exam details for the timer"""
        if "user" not in session:
            return redirect(url_for("login"))

        exam = self.db.fetch_one("SELECT * FROM exam WHERE e_id = %s", (e_id,))
        if exam:
            return render_template("exam_timer.html", exam=exam)
        return redirect(url_for("exam"))


