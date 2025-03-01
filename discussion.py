from flask import Flask, session, render_template, redirect, url_for, jsonify, request
from database import DatabaseManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security

db = DatabaseManager()


class DiscussionManager:
    def __init__(self):
        self.db = db

    def get_discussions(self):
        """Fetch all discussions and display in HTML"""
        if "user" in session:
            discussions = self.db.fetch_all("""
                SELECT d.d_id, d.dtask_name, t.task_name AS related_task, d.ddate, d.dpriority, d.dstatus
                FROM discussion d
                JOIN tasks t ON d.task_id = t.task_id
            """)
            tasks = self.db.fetch_all("SELECT task_id, task_name FROM tasks")  # Fetch tasks for dropdown
            return render_template("discussion.html", discussions=discussions, tasks=tasks)
        return redirect(url_for("login"))

    def add_discussion(self):
        """Add a new discussion and update the progress table"""
        if "user" in session:
            try:
                data = request.form
                insert_query = """
                INSERT INTO discussion (dtask_name, task_id, ddate, dpriority, dstatus)
                VALUES (%s, %s, %s, %s, 'Pending')
                """
                if self.db.execute_query(insert_query, (data["discussion_name"], data["task_id"], data["date"], data["priority"])):
                    last_discussion = self.db.fetch_one("SELECT LAST_INSERT_ID() as d_id")
                    if last_discussion:
                        d_id = last_discussion["d_id"]
                        self.db.execute_query("INSERT INTO progress (d_id) VALUES (%s)", (d_id,))
                        print(f"✅ Discussion added with d_id: {d_id}, also added to progress table.")  # Debugging log

                    updated_discussions = self.db.fetch_all("SELECT * FROM discussion")
                    return jsonify(success=True, message="Discussion added successfully!", discussions=updated_discussions)

            except Exception as e:
                print(f"❌ Error adding discussion: {str(e)}")  # Debugging log
                return jsonify(success=False, message="Error adding discussion!")

        return jsonify(success=False, message="Unauthorized")

    def delete_discussion(self, d_id):
        """Delete a discussion and remove it from progress"""
        if "user" in session:
            try:
                discussion = self.db.fetch_one("SELECT * FROM discussion WHERE d_id = %s", (d_id,))
                if not discussion:
                    return jsonify(success=False, message="Discussion not found!")

                self.db.execute_query("DELETE FROM progress WHERE d_id = %s", (d_id,))  # Remove from progress
                self.db.execute_query("DELETE FROM discussion WHERE d_id = %s", (d_id,))  # Remove discussion
                print(f"✅ Discussion with d_id {d_id} deleted successfully from both tables.")  # Debugging log

                updated_discussions = self.db.fetch_all("SELECT * FROM discussion")
                return jsonify(success=True, discussions=updated_discussions)

            except Exception as e:
                print(f"❌ Error deleting discussion: {str(e)}")  # Debugging log
                return jsonify(success=False, message="Error deleting discussion!")

        return jsonify(success=False, message="Unauthorized")


# Create Discussion Manager instance
discussion_manager = DiscussionManager()

