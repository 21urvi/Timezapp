from flask import Flask, session, render_template, redirect, url_for, request, jsonify
from database import DatabaseManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security

db = DatabaseManager()


class ExamTaskManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_exams(self):
        """Fetch all exam tasks"""
        if "user" not in session:
            return redirect(url_for("login"))

        try:
            exams = self.db.fetch_all("SELECT * FROM exam")
            return render_template("exam.html", exams=exams)
        except Exception as e:
            print(f"❌ Error fetching exams: {str(e)}")
            return jsonify(success=False, message="Error fetching exams!")

    def get_exams_json(self):
        """Fetch all exam tasks as JSON for FullCalendar"""
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 403

        try:
            exams = self.db.fetch_all("SELECT e_id, etask_name, edate FROM exam")
            return jsonify([
                {"id": exam["e_id"], "title": exam["etask_name"], "start": exam["edate"].strftime('%Y-%m-%d')}
                for exam in exams
            ])
        except Exception as e:
            print(f"❌ Error fetching exam JSON: {str(e)}")
            return jsonify(success=False, message="Error fetching exams!")

    def add_exam_task(self):
        """Add a new exam task"""
        if "user" in session:
            try:
                data = request.form  # ✅ Ensure we receive form data properly

                # ✅ Validate that all required fields are present
                if not data.get("etask_name") or not data.get("edate") or not data.get("epriority"):
                    return jsonify(success=False, message="Missing required fields.")

                insert_query = """
                    INSERT INTO exam (etask_name, edate, epriority, estatus) 
                    VALUES (%s, %s, %s, 'Incomplete')
                """

                # ✅ Execute the query
                self.db.execute_query(insert_query, (data["etask_name"], data["edate"], data["epriority"]))

                # ✅ Fetch the last inserted exam to return it
                last_exam = self.db.fetch_one("SELECT * FROM exam ORDER BY e_id DESC LIMIT 1")

                return jsonify(success=True, message="Exam task added successfully!", exam=last_exam)

            except Exception as e:
                print(f"❌ Error adding exam: {str(e)}")  # Debugging
                return jsonify(success=False, message="Error adding exam.")

        return jsonify(success=False, message="Unauthorized")

    def fetch_exam_task_by_id(self, e_id):
        """Fetch a specific exam task by ID (for validation before deletion)"""
        try:
            return self.db.fetch_one("SELECT * FROM exam WHERE e_id = %s", (e_id,))
        except Exception as e:
            print(f"❌ Error fetching exam by ID {e_id}: {str(e)}")
            return None

    def delete_exam_task(self, e_id):
        """Delete an exam task and remove it from progress"""
        if "user" not in session:
            return jsonify(success=False, message="Unauthorized")

        try:
            task = self.fetch_exam_task_by_id(e_id)
            if not task:
                return jsonify(success=False, message="Task not found!")

            # ✅ Delete from progress first
            self.db.execute_query("DELETE FROM progress WHERE e_id = %s", (e_id,))

            # ✅ Then delete from exam table
            self.db.execute_query("DELETE FROM exam WHERE e_id = %s", (e_id,))
            print(f"✅ Task with e_id {e_id} deleted successfully.")  # Debugging log

            # ✅ Fetch updated exams list
            updated_exams = self.db.fetch_all("SELECT * FROM exam")

            # ✅ Return the updated list
            return jsonify(success=True, message="Exam task deleted successfully!", exams=updated_exams)

        except Exception as e:
            print(f"❌ Error deleting task: {str(e)}")  # Debugging log
            return jsonify(success=False, message="Error deleting task!")

