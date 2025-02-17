'''from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import random, string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'  # Change if using a different host
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'urvi2115'
app.config['MYSQL_DB'] = 'timezap'

mysql = MySQL(app)

# Generate CAPTCHA
def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user_captcha = request.form['captcha']
        stored_captcha = session.get('captcha')

        # Check CAPTCHA
        if user_captcha != stored_captcha:
            msg = 'Incorrect CAPTCHA. Try again.'
        else:
            # Store user credentials in the database
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
            mysql.connection.commit()
            cursor.close()

            session['user'] = email
            return redirect(url_for('welcome'))  # Redirect to welcome page after login

    session['captcha'] = generate_captcha()  # Refresh CAPTCHA
    return render_template('login.html', captcha=session['captcha'], msg=msg)

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if 'user' in session:
        if request.method == 'POST':
            return redirect(url_for('timer'))  # Redirect to timer on button click
        return render_template('welcome.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/')
def otimer():
    return render_template('otimer.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)'''

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
import random, string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="urvi2115",
    database="timezap"
)
cursor = db.cursor()


# Generate CAPTCHA
def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# ---------- USER AUTHENTICATION ----------
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user_captcha = request.form['captcha']
        stored_captcha = session.get('captcha')

        if user_captcha != stored_captcha:
            msg = 'Incorrect CAPTCHA. Try again.'
        else:
            cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
            db.commit()
            session['user'] = email
            return redirect(url_for('welcome'))

    session['captcha'] = generate_captcha()
    return render_template('login.html', captcha=session['captcha'], msg=msg)


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if 'user' in session:
        if request.method == 'POST':
            return redirect(url_for('home'))
        return render_template('welcome.html', user=session['user'])
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ---------- TASK MANAGEMENT ----------
@app.route("/tasks")
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template("tasks.html", tasks=tasks)


@app.route("/timer/<int:task_id>")
def timer(task_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    task = cursor.fetchone()

    if task:
        return render_template("timer.html", task=task)
    return redirect(url_for("home"))


@app.route("/add", methods=["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for('login'))

    data = request.form
    cursor.execute("INSERT INTO tasks (task_name, date, priority, status) VALUES (%s, %s, %s, 'Incomplete')",
                   (data["task_name"], data["date"], data["priority"]))
    db.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if 'user' not in session:
        return jsonify(success=False, message="Unauthorized"), 403

    cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
    db.commit()
    return jsonify(success=True)


@app.route("/update_status", methods=["POST"])
def update_status():
    if 'user' not in session:
        return jsonify(success=False, message="Unauthorized"), 403

    data = request.json
    cursor.execute("UPDATE tasks SET status = %s WHERE task_id = %s", (data["status"], data["task_id"]))
    db.commit()
    return jsonify(success=True)


# ---------- PRACTICAL TASK MANAGEMENT ----------
@app.route("/practical")
def practical():
    if "user" in session:
        cursor.execute("SELECT * FROM practical")
        practicals = cursor.fetchall()
        return render_template("practical.html", practicals=practicals)
    return redirect(url_for("login"))


@app.route("/add_practical", methods=["POST"])
def add_practical():
    if "user" in session:
        data = request.form
        cursor.execute(
            "INSERT INTO practical (ptask_name, p_date, p_priority, p_status) VALUES (%s, %s, %s, 'Incomplete')",
            (data["task_name"], data["date"], data["priority"]))
        db.commit()
        return redirect(url_for("practical"))
    return redirect(url_for("login"))


@app.route("/delete_practical/<int:p_id>", methods=["DELETE"])
def delete_practical(p_id):
    if "user" in session:
        cursor.execute("DELETE FROM practical WHERE p_id = %s", (p_id,))
        db.commit()
        return jsonify(success=True)
    return jsonify(success=False, message="Unauthorized")


@app.route("/practical_timer/<int:p_id>")
def practical_timer(p_id):
    if "user" in session:
        cursor.execute("SELECT * FROM practical WHERE p_id = %s", (p_id,))
        practical = cursor.fetchone()
        if practical:
            return render_template("practical_timer.html", practical=practical)
        return redirect(url_for("practical"))
    return redirect(url_for("login"))


# ---------- DEFAULT ROUTES ----------
@app.route('/otimer')
def otimer():
    return render_template('otimer.html')


@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/revision')
def revision():
    return render_template('revision.html')


# ---------- RUN SERVER ----------
if __name__ == '__main__':
    app.run(debug=True)

