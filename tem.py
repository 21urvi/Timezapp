
from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="urvi2115",
    database="timezap"
)
cursor = db.cursor()

# Home Route (Task Page)
@app.route("/")
def home():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template("tasks.html", tasks=tasks)

# Timer for task Page
@app.route("/timer/<int:task_id>")
def timer(task_id):
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    task = cursor.fetchone()
    if task:
        return render_template("timer.html", task=task)
    return redirect(url_for("home"))

# Add Task Route
@app.route("/add", methods=["POST"])
def add_task():
    data = request.form
    cursor.execute("INSERT INTO tasks (task_name, date, priority, status) VALUES (%s, %s, %s, 'Incomplete')",
                   (data["task_name"], data["date"], data["priority"]))
    db.commit()
    return redirect(url_for("home"))

# Delete Task Route
@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
    db.commit()
    return jsonify(success=True)

# Update Task Status Route
@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.json
    cursor.execute("UPDATE tasks SET status = %s WHERE task_id = %s", (data["status"], data["task_id"]))
    db.commit()
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)


