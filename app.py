import mysql
from flask import Flask, request, session, render_template, redirect, url_for, jsonify
from flask_cors import CORS
from project.database import DatabaseManager
from user import UserManager
from task import TaskManager
from practical import PracticalTaskManager
from revision import RevisionTaskManager
from subject import SubjectManager
from exam import ExamTaskManager
from discussion import DiscussionManager
from timer import TimerManager
from calendar_manager import CalendarManager
from progress import get_progress_data

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

# Instantiate Managers
db_manager = DatabaseManager()
user_manager = UserManager()
task_manager = TaskManager()
practical_manager = PracticalTaskManager()
revision_manager = RevisionTaskManager()
subject_manager = SubjectManager()
exam_manager = ExamTaskManager()
discussion_manager = DiscussionManager()
timer_manager = TimerManager()
calendar_manager = CalendarManager()

# --------- USER AUTHENTICATION ---------
@app.route('/', methods=['GET', 'POST'])
def login():
    return user_manager.login_user(request)

@app.route('/logout')
def logout():
    """Clear session and redirect to login"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/welcome', methods=['GET'])
def welcome():
    if session.get('user'):
        return render_template('welcome.html', user=session['user'])
    return redirect(url_for('login'))

# --------- OTIMER PAGE ---------
@app.route('/otimer', methods=['GET'])
def otimer():
    return render_template('otimer.html')

# --------- TASK MANAGEMENT ---------

@app.route("/tasks")
def tasks():
    return task_manager.get_tasks()

@app.route("/tasks_json")
def tasks_json():
    return task_manager.get_tasks_json()

@app.route("/add_task", methods=["POST"])
def add_task():
    return task_manager.add_task()

@app.route("/delete_task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    return task_manager.delete_task(task_id)


# --------- PRACTICAL TASK MANAGEMENT ---------
@app.route("/practical")
def practical_page():
    return practical_manager.get_practical_tasks()

@app.route("/add_practical", methods=["POST"])
def add_practical():
    return practical_manager.add_practical_task()

@app.route("/delete_practical/<int:p_id>", methods=["DELETE"])
def delete_practical(p_id):
    return practical_manager.delete_practical_task(p_id)

@app.route('/get_practical_tasks_json', methods=['GET'])
def get_practical_tasks_json():
    return practical_manager.get_practical_tasks_json()

# --------- REVISION TASK MANAGEMENT ---------
@app.route("/revision")
def revision():
    return revision_manager.get_revisions()

@app.route("/add_revision", methods=["POST"])
def add_revision():
    return revision_manager.add_revision_task()

@app.route("/delete_revision/<int:r_id>", methods=["DELETE"])
def delete_revision(r_id):
    return revision_manager.delete_revision_task(r_id)

# --------- SUBJECT TASK MANAGEMENT ---------

@app.route("/subject")
def subject():
    return subject_manager.get_subjects()


@app.route("/subjects_json")
def subjects_json():
    return subject_manager.get_subjects_json()


@app.route("/add_subject", methods=["POST"])
def add_subject():
    return subject_manager.add_subject()


@app.route("/delete_subject/<int:s_id>", methods=["DELETE"])
def delete_subject(s_id):
    return subject_manager.delete_subject(s_id)




# --------- EXAM MANAGEMENT ---------
@app.route("/exam")
def exam():
    """Route to fetch all exam tasks and render the exam page."""
    return exam_manager.get_exams()

@app.route("/exams_json")
def exams_json():
    """Route to fetch all exam tasks as JSON (used for FullCalendar)."""
    return exam_manager.get_exams_json()

@app.route("/add_exam", methods=["POST"])
def add_exam():
    """Route to add a new exam task."""
    return exam_manager.add_exam_task()

@app.route("/delete_exam/<int:e_id>", methods=["DELETE"])
def delete_exam(e_id):
    """Route to delete an exam task."""
    return exam_manager.delete_exam_task(e_id)



# --------- DISCUSSION MANAGEMENT ---------

@app.route("/discussion")
def discussion():
    """Render the discussion page"""
    return discussion_manager.get_discussions()

@app.route("/add_discussion", methods=["POST"])
def add_discussion():
    """Handle adding a new discussion"""
    return discussion_manager.add_discussion()

@app.route("/delete_discussion/<int:d_id>", methods=["POST"])  # Changed DELETE to POST for broader support
def delete_discussion(d_id):
    """Handle deleting a discussion"""
    return discussion_manager.delete_discussion(d_id)


# --------- TIMER ---------
@app.route("/timer/<int:task_id>", methods=['GET'])
def task_timer(task_id):
    return timer_manager.get_task_timer(task_id)

@app.route("/practical_timer/<int:p_id>", methods=['GET'])
def practical_timer(p_id):
    return timer_manager.get_practical_timer(p_id)

@app.route("/revision_timer/<int:r_id>", methods=['GET'])
def revision_timer(r_id):
    return timer_manager.get_revision_timer(r_id)

@app.route("/subject_timer/<int:s_id>", methods=['GET'])
def subject_timer(s_id):
    return timer_manager.get_subject_timer(s_id)

@app.route("/exam_timer/<int:e_id>", methods=['GET'])
def exam_timer(e_id):
    return timer_manager.get_exam_timer(e_id)

@app.route("/discussion_timer/<int:d_id>", methods=['GET'])
def discussion_timer(d_id):
    return timer_manager.get_discussion_timer(d_id)

# --------- CALENDAR ---------
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/fetch_tasks')
def fetch_tasks():
    return calendar_manager.fetch_tasks()

# --------- PROGRESS ---------
@app.route('/progress')
def progress():
    return render_template('progress.html')


@app.route('/progress-data')
def progress_data():
    """API endpoint to return progress data as JSON."""
    return jsonify(get_progress_data())

# --------- RUN SERVER ---------
if __name__ == '__main__':
    app.run(debug=True)
