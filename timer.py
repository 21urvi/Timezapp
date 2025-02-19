from flask import session, render_template, redirect, url_for
from database import DatabaseManager

class TimerManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_task_timer(self, task_id):
        if 'user' not in session:
            return redirect(url_for('login'))

        task = self.db.fetch_one("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        if task:
            return render_template("timer.html", task=task, task_type="Task")
        return redirect(url_for("home"))

    def get_practical_timer(self, p_id):
        if "user" not in session:
            return redirect(url_for("login"))

        practical = self.db.fetch_one("SELECT * FROM practical WHERE p_id = %s", (p_id,))
        if practical:
            return render_template("timer.html", task=practical, task_type="Practical")
        return redirect(url_for("practical"))

    def get_revision_timer(self, r_id):
        if "user" not in session:
            return redirect(url_for("login"))

        revision = self.db.fetch_one("SELECT * FROM revision WHERE r_id = %s", (r_id,))
        if revision:
            return render_template("timer.html", task=revision, task_type="Revision")
        return redirect(url_for("revision"))

    def get_subject_timer(self, s_id):
        if "user" not in session:
            return redirect(url_for("login"))

        subject = self.db.fetch_one("SELECT * FROM subject WHERE s_id = %s", (s_id,))
        if subject:
            return render_template("timer.html", task=subject, task_type="Subject")
        return redirect(url_for("subject"))

    def get_exam_timer(self, e_id):
        if "user" not in session:
            return redirect(url_for("login"))

        exam = self.db.fetch_one("SELECT * FROM exam WHERE e_id = %s", (e_id,))
        if exam:
            return render_template("timer.html", task=exam, task_type="Exam")
        return redirect(url_for("exam"))

    def get_discussion_timer(self, d_id):
        if "user" not in session:
            return redirect(url_for("login"))

        discussion = self.db.fetch_one("SELECT * FROM discussion WHERE d_id = %s", (d_id,))
        if discussion:
            return render_template("timer.html", task=discussion, task_type="Discussion")
        return redirect(url_for("discussion"))
