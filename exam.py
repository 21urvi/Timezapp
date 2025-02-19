from flask import Flask, session, render_template, redirect, url_for, request, jsonify
from database import DatabaseManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security
db = DatabaseManager()


class ExamTaskManager:
    def __init__(self):
        self.db = db

    def get_exams(self):
        """Fetch all exam tasks"""
        if 'user' not in session:
            return redirect(url_for('login'))
        exams = self.db.fetch_all("SELECT * FROM exam")
        return render_template("exam.html", exams=exams)

    def add_exam(self, request):
        """Add a new exam task"""
        if 'user' not in session:
            return redirect(url_for('login'))

        data = request.form
        self.db.execute_query(
            "INSERT INTO exam (etask_name, edate, epriority, estatus) VALUES (%s, %s, %s, 'Incomplete')",
            (data["etask_name"], data["edate"], data["epriority"])
        )
        return redirect(url_for("exam"))

    def delete_exam(self, e_id):
        """Delete an exam task"""
        if 'user' not in session:
            return jsonify(success=False, message="Unauthorized"), 403

        self.db.execute_query("DELETE FROM exam WHERE e_id = %s", (e_id,))
        return jsonify(success=True)


exam_manager = ExamTaskManager()

@app.route("/exam")
def exam():
    return exam_manager.get_exams()

@app.route("/add_exam", methods=["POST"])
def add_exam():
    return exam_manager.add_exam(request)

@app.route("/delete_exam/<int:e_id>", methods=["DELETE"])
def delete_exam(e_id):
    return exam_manager.delete_exam(e_id)
