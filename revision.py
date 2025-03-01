from flask import session, render_template, redirect, url_for, request, jsonify
from database import DatabaseManager

class RevisionTaskManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_revisions(self):
        """Fetch all revision tasks"""
        if "user" in session:
            revisions = self.db.fetch_all("SELECT * FROM revision")
            return render_template("revision.html", revisions=revisions)
        return redirect(url_for("login"))

    def get_revisions_json(self):
        """Fetch all revision tasks as JSON (For FullCalendar or API)"""
        if "user" in session:
            revisions = self.db.fetch_all("SELECT r_id, rtask_name, rdate FROM revision")
            return jsonify([
                {"id": r["r_id"], "title": r["rtask_name"], "start": r["rdate"].strftime('%Y-%m-%d')}
                for r in revisions
            ])
        return jsonify({"error": "Unauthorized"}), 403

    def add_revision_task(self):
        """Add a new revision task"""
        if "user" not in session:
            return jsonify(success=False, message="Unauthorized"), 401

        try:
            data = request.form if request.form else request.get_json()  # ✅ Accept both form-data & JSON

            if not data or "rtask_name" not in data or "rdate" not in data:
                return jsonify(success=False, message="Missing required fields"), 400

            insert_query = """
                INSERT INTO revision (rtask_name, rdate, rpriority, focus_point, rstatus) 
                VALUES (%s, %s, %s, %s, 'Incomplete')
            """
            success = self.db.execute_query(insert_query,
                                            (data["rtask_name"], data["rdate"], data.get("rpriority", "Low"),
                                             data.get("focus_point", "")))

            if success:
                last_revision = self.db.fetch_one("SELECT LAST_INSERT_ID() as r_id")
                if last_revision:
                    r_id = last_revision["r_id"]
                    self.db.execute_query("INSERT INTO progress (r_id) VALUES (%s)", (r_id,))
                    print(f"✅ Revision task added with r_id: {r_id}")  # Debugging log

                updated_revisions = self.db.fetch_all("SELECT * FROM revision")
                return jsonify(success=True, message="Task added successfully!", revisions=updated_revisions)

        except Exception as e:
            print(f"❌ Error adding revision: {str(e)}")  # Debugging log
            return jsonify(success=False, message="Error adding revision task!"), 500

    def delete_revision_task(self, r_id):
        """Delete a revision task"""
        if "user" not in session:
            return jsonify(success=False, message="Unauthorized"), 401

        try:
            task_exists = self.db.fetch_one("SELECT * FROM revision WHERE r_id = %s", (r_id,))
            if not task_exists:
                return jsonify(success=False, message="Task not found"), 404

            self.db.execute_query("DELETE FROM progress WHERE r_id = %s", (r_id,))
            self.db.execute_query("DELETE FROM revision WHERE r_id = %s", (r_id,))
            print(f"✅ Revision task with r_id {r_id} deleted successfully.")  # Debugging log

            updated_revisions = self.db.fetch_all("SELECT * FROM revision")
            return jsonify(success=True, message="Task deleted successfully!", revisions=updated_revisions)

        except Exception as e:
            print(f"❌ Error deleting revision task: {str(e)}")  # Debugging log
            return jsonify(success=False, message="Error deleting task!"), 500
