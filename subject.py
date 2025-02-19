from flask import Flask, session, render_template, redirect, url_for, request, jsonify
from database import DatabaseManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security
db = DatabaseManager()


class SubjectTaskManager:
    def __init__(self):
        self.db = db

    def get_subjects(self):
        """Fetch all subject tasks"""
        if 'user' not in session:
            return redirect(url_for('login'))
        subjects = self.db.fetch_all("SELECT * FROM subject")
        return render_template("subject.html", subjects=subjects)

    def add_subject(self, request):
        """Add a new subject task"""
        if 'user' not in session:
            return redirect(url_for('login'))

        data = request.form
        self.db.execute_query(
            "INSERT INTO subject (subject, stask_name, sdate, spriority, sstatus) VALUES (%s, %s, %s, %s, 'Incomplete')",
            (data["subject"], data["stask_name"], data["sdate"], data["spriority"])
        )
        return redirect(url_for("subject"))

    def delete_subject(self, s_id):
        """Delete a subject task"""
        if 'user' not in session:
            return jsonify(success=False, message="Unauthorized"), 403

        self.db.execute_query("DELETE FROM subject WHERE s_id = %s", (s_id,))
        return jsonify(success=True)

subject_manager = SubjectTaskManager()

@app.route("/subject")
def subject():
    return subject_manager.get_subjects()

@app.route("/add_subject", methods=["POST"])
def add_subject():
    return subject_manager.add_subject(request)

@app.route("/delete_subject/<int:s_id>", methods=["DELETE"])
def delete_subject(s_id):
    return subject_manager.delete_subject(s_id)
