from flask import Flask, session, render_template, redirect, url_for, request, jsonify
from database import DatabaseManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security

db = DatabaseManager()


class SubjectManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_subjects(self):
        """Fetch all subjects and display them"""
        if "user" in session:
            subjects = self.db.fetch_all("""
                SELECT s.s_id, s.subject, s.stask_name, s.sdate, s.spriority, s.sstatus, 
                       COALESCE(p.progress, 0) AS progress
                FROM subject s
                LEFT JOIN progress p ON s.s_id = p.s_id
                ORDER BY s.s_id DESC
            """)
            return render_template("subject.html", subjects=subjects)
        return redirect(url_for("login"))

    def get_subjects_json(self):
        """Fetch subjects as JSON"""
        if "user" in session:
            subjects = self.db.fetch_all("SELECT * FROM subject")
            return jsonify(subjects)
        return jsonify({"error": "Unauthorized"}), 403

    def add_subject(self):
        """Add a new subject task"""
        if "user" not in session:
            return jsonify(success=False, message="Unauthorized")

        try:
            data = request.form  # ✅ FIXED: Changed from request.json to request.form
            subject = data.get("subject")
            stask_name = data.get("stask_name")
            sdate = data.get("sdate")
            spriority = data.get("spriority")

            if not (subject and stask_name and sdate and spriority):
                return jsonify(success=False, message="Missing required fields!")

            # Insert into subject table
            insert_query = """
                INSERT INTO subject (subject, stask_name, sdate, spriority, sstatus) 
                VALUES (%s, %s, %s, %s, 'Incomplete')
            """
            self.db.execute_query(insert_query, (subject, stask_name, sdate, spriority))

            return jsonify(success=True, message="Subject added successfully!")

        except Exception as e:
            return jsonify(success=False, message="Error adding subject!", error=str(e))

    def delete_subject(self, s_id):
        """Delete a subject"""
        if "user" not in session:
            return jsonify(success=False, message="Unauthorized")

        try:
            subject = self.db.fetch_one("SELECT * FROM subject WHERE s_id = %s", (s_id,))
            if not subject:
                return jsonify(success=False, message="Subject not found!")

            self.db.execute_query("DELETE FROM progress WHERE s_id = %s", (s_id,))
            self.db.execute_query("DELETE FROM subject WHERE s_id = %s", (s_id,))

            return jsonify(success=True, message="Subject deleted successfully!")

        except Exception as e:
            return jsonify(success=False, message="Error deleting subject!", error=str(e))
