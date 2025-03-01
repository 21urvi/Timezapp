from flask import session, render_template, redirect, url_for, request, jsonify
from database import DatabaseManager

class PracticalTaskManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_practical_tasks(self):
        """Fetch all practical tasks"""
        if "user" in session:
            practicals = self.db.fetch_all("SELECT * FROM practical")
            return render_template("practical.html", practicals=practicals)
        return redirect(url_for("login"))

    def get_practical_tasks_json(self):
        """Fetch all practical tasks as JSON for FullCalendar"""
        if "user" in session:
            practicals = self.db.fetch_all("SELECT p_id, ptask_name, p_date FROM practical")
            return jsonify([
                {"id": p["p_id"], "title": p["ptask_name"], "start": p["p_date"].strftime('%Y-%m-%d')}
                for p in practicals
            ])
        return jsonify({"error": "Unauthorized"}), 403

    def add_practical_task(self):
        """Add a new practical task and update progress table"""
        if "user" in session:
            try:
                data = request.form
                insert_query = """
                    INSERT INTO practical (ptask_name, p_date, p_priority, p_status) 
                    VALUES (%s, %s, %s, 'Incomplete')
                """
                if self.db.execute_query(insert_query, (data["task_name"], data["date"], data["priority"])):
                    last_practical = self.db.fetch_one("SELECT LAST_INSERT_ID() as p_id")
                    if last_practical:
                        p_id = last_practical["p_id"]
                        self.db.execute_query("INSERT INTO progress (p_id) VALUES (%s)", (p_id,))
                        print(f"✅ Practical task added with p_id: {p_id}")  # Debugging log

                    updated_practicals = self.db.fetch_all("SELECT * FROM practical")
                    return jsonify(success=True, message="Practical task added successfully!", practicals=updated_practicals)

            except Exception as e:
                print(f"❌ Error adding task: {str(e)}")  # Debugging log
                return jsonify(success=False, message="Error adding task!")

        return jsonify(success=False, message="Unauthorized")

    def fetch_practical_task_by_id(self, p_id):
        """Fetch a specific practical task by ID (for validation before deletion)"""
        return self.db.fetch_one("SELECT * FROM practical WHERE p_id = %s", (p_id,))

    def delete_practical_task(self, p_id):
        """Delete a practical task and remove it from progress"""
        if "user" in session:
            try:
                task = self.fetch_practical_task_by_id(p_id)
                if not task:
                    return jsonify(success=False, message="Task not found!")

                self.db.execute_query("DELETE FROM progress WHERE p_id = %s", (p_id,))
                self.db.execute_query("DELETE FROM practical WHERE p_id = %s", (p_id,))
                print(f"✅ Task with p_id {p_id} deleted successfully.")  # Debugging log

                updated_practicals = self.db.fetch_all("SELECT * FROM practical")
                return jsonify(success=True, practicals=updated_practicals)

            except Exception as e:
                print(f"❌ Error deleting task: {str(e)}")  # Debugging log
                return jsonify(success=False, message="Error deleting task!")

        return jsonify(success=False, message="Unauthorized")
