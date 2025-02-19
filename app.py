from flask import Flask, request, session, render_template, redirect, url_for, jsonify
from user import UserManager
from task import TaskManager
from practical import PracticalTaskManager
from revision import RevisionTaskManager
from subject import SubjectTaskManager
from exam import ExamTaskManager
from discussion import DiscussionManager
from timer import TimerManager
from calendar_manager import CalendarManager
from progress import ProgressManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Instantiate Managers
user_manager = UserManager()
task_manager = TaskManager()
practical_manager = PracticalTaskManager()
revision_manager = RevisionTaskManager()
subject_manager = SubjectTaskManager()
exam_manager = ExamTaskManager()
discussion_manager = DiscussionManager()
timer_manager = TimerManager()
calendar_manager = CalendarManager()
progress_manager = ProgressManager()

# --------- USER AUTHENTICATION ---------
@app.route('/', methods=['GET', 'POST'])
def login():
    return user_manager.login_user(request)

@app.route('/logout', methods=['POST'])
def logout():
    return user_manager.logout_user()

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
@app.route("/tasks", methods=['GET'])
def home():
    return task_manager.get_tasks()

@app.route("/add", methods=["POST"])
def add_task():
    return task_manager.add_task(request)

@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    return task_manager.delete_task(task_id)

# --------- PRACTICAL TASK MANAGEMENT ---------
@app.route("/practical", methods=['GET'])
def practical():
    return practical_manager.get_practical_tasks()

@app.route("/add_practical", methods=["POST"])
def add_practical():
    return practical_manager.add_practical_task(request)

@app.route("/delete_practical/<int:p_id>", methods=["DELETE"])
def delete_practical(p_id):
    return practical_manager.delete_practical_task(p_id)

# --------- REVISION TASK MANAGEMENT ---------
@app.route("/revision", methods=['GET'])
def revision():
    return revision_manager.get_revisions()

@app.route("/add_revision", methods=["POST"])
def add_revision():
    return revision_manager.add_revision(request)

@app.route("/delete_revision/<int:r_id>", methods=["DELETE"])
def delete_revision(r_id):
    return revision_manager.delete_revision(r_id)

# --------- SUBJECT TASK MANAGEMENT ---------
@app.route("/subject", methods=['GET'])
def subject():
    return subject_manager.get_subjects()

@app.route("/add_subject", methods=["POST"])
def add_subject():
    return subject_manager.add_subject(request)

@app.route("/delete_subject/<int:s_id>", methods=["DELETE"])
def delete_subject(s_id):
    return subject_manager.delete_subject(s_id)

# --------- EXAM MANAGEMENT ---------
@app.route("/exam", methods=['GET'])
def exam():
    return exam_manager.get_exams()

@app.route("/add_exam", methods=["POST"])
def add_exam():
    return exam_manager.add_exam(request)

@app.route("/delete_exam/<int:e_id>", methods=["DELETE"])
def delete_exam(e_id):
    return exam_manager.delete_exam(e_id)

# --------- DISCUSSION MANAGEMENT ---------
@app.route("/discussion", methods=['GET'])
def discussion():
    return discussion_manager.get_discussions()

@app.route("/add_discussion", methods=["POST"])
def add_discussion():
    return discussion_manager.add_discussion()

@app.route("/delete_discussion/<int:d_id>", methods=["DELETE"])
def delete_discussion(d_id):
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
@app.route('/calendar', methods=['GET'])
def calendar():
    return calendar_manager.show_calendar()

# --------- PROGRESS ---------
@app.route('/progress', methods=['GET'])
def progress():
    return progress_manager.show_progress()

# --------- RUN SERVER ---------
if __name__ == '__main__':
    app.run(debug=True)
