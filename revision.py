from flask import Flask, session, render_template, redirect, url_for, request, jsonify
from database import DatabaseManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security
db = DatabaseManager()


class RevisionTaskManager:
    def __init__(self):
        self.db = db

    def get_revisions(self):
        """Fetch all revision tasks"""
        if 'user' not in session:
            return redirect(url_for('login'))
        revisions = self.db.fetch_all("SELECT * FROM revision")
        return render_template("revision.html", revisions=revisions)

    def add_revision(self, request):
        """Add a new revision task"""
        if 'user' not in session:
            return redirect(url_for('login'))

        data = request.form
        self.db.execute_query(
            "INSERT INTO revision (rtask_name, rdate, rpriority, focus_point, rstatus) VALUES (%s, %s, %s, %s, "
            "'Incomplete')",
            (data["rtask_name"], data["rdate"], data["rpriority"], data["focus_point"])
        )
        return redirect(url_for("revision"))

    def delete_revision(self, rid):
        """Delete a revision task"""
        if 'user' not in session:
            return jsonify(success=False, message="Unauthorized"), 403

        self.db.execute_query("DELETE FROM revision WHERE rid = %s", (rid,))
        return jsonify(success=True)


