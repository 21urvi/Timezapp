from flask import Flask, render_template, request, redirect, session, flash, url_for, send_file
import mysql.connector
import bcrypt
import random
import string
import io
from captcha.image import ImageCaptcha

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # Change this to your MySQL username
    "password": "urvi2115",  # Change this to your MySQL password
    "database": "timezap"
}

# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Function to generate CAPTCHA text
def generate_captcha_text():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    session['captcha_answer'] = captcha_text
    return captcha_text

# Route to generate CAPTCHA image
@app.route('/captcha')
def captcha():
    image = ImageCaptcha(width=280, height=90)
    captcha_text = generate_captcha_text()
    data = image.generate(captcha_text)
    return send_file(io.BytesIO(data.getvalue()), mimetype='image/png')

# Route for login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        gmail = request.form["gmail"]  # Changed from 'email' to 'gmail'
        password = request.form["password"]
        captcha_response = request.form["captcha"]

        # Validate CAPTCHA
        if captcha_response.upper() != session.get('captcha_answer', ''):
            flash("Incorrect CAPTCHA. Try again!", "danger")
            return redirect(url_for("login"))

        # Check user credentials in the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login WHERE gmail = %s", (gmail,))  # Changed column name to 'gmail'
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):  # Ensure hashed passwords
            session["user"] = gmail
            return redirect(url_for("welcome"))
        else:
            flash("Invalid Gmail or password", "danger")  # Updated message
            return redirect(url_for("login"))

    return render_template("login.html")

# Route for dashboard
@app.route("/welcome")
def welcome():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("welcome.html", user=session["user"])

# Logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)





'''from flask import Flask, render_template, request, session, redirect, \
    url_for, flash, jsonify,send_file
from flask_mysqldb import MySQL
from PIL import Image, ImageDraw, ImageFont
import random
import string
import os
import time
import threading


# Login
app = Flask(__name__)
app.secret_key = 'your_secret_key'

#---------------------------------------------------------------------------------------index

@app.route('/')
def index():
    return render_template('index.html')

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'  # MySQL server's host
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'timer'  # The database name

# Initialize MySQL
mysql = MySQL(app)


# Function to generate a random CAPTCHA text
def generate_captcha_text(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Function to create CAPTCHA image
def create_captcha(text):
    width, height = 150, 50
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for i in range(5):  # Random noise
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(0, 0, 0), width=1)

    draw.text((30, 15), text, font=font, fill=(0, 0, 0))

    captcha_path = "static/captcha.png"
    image.save(captcha_path)
    return captcha_path


@app.route('/captcha')
def captcha():
    captcha_text = generate_captcha_text()
    session['captcha'] = captcha_text  # Store in session
    create_captcha(captcha_text)
    return send_file("static/captcha.png", mimetype='image/png')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_captcha = request.form['captcha']

        if user_captcha.upper() == session.get('captcha'):
            # Connect to MySQL and verify the login credentials
            cur = mysql.connection.cursor()

            # Query to check if the email and password match a user in the database
            cur.execute("SELECT * FROM login WHERE email = %s AND password = %s", (email, password))

            user = cur.fetchone()

            if user:
                return "Login Successful!"
            else:
                flash("Incorrect email or password.")

            # Close the cursor
            cur.close()

        else:
            flash("Incorrect CAPTCHA. Try again.")

    return render_template('login.html')


# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_captcha = request.form['captcha']

        # Validate CAPTCHA
        if user_captcha.upper() == session.get('captcha'):
            # Insert new user into the database
            cur = mysql.connection.cursor()

            # Check if the email already exists
            cur.execute("SELECT * FROM login WHERE email = %s", (email,))
            existing_user = cur.fetchone()
            if existing_user:
                flash("Email already registered.")
                cur.close()
                return redirect(url_for('register'))

            # Insert the new user into the users table
            cur.execute("INSERT INTO login (email, password) VALUES (%s, %s)", (email, password))
            mysql.connection.commit()  # Commit the transaction

            flash("Registration successful! Please login.")
            cur.close()

            return redirect(url_for('login'))

        else:
            flash("Incorrect CAPTCHA. Try again.")

    return render_template('register.html')


#----------------------------------------------------------------------------------------Task

# Secret key for session management
app.secret_key = os.urandom(24)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'  # or the host of your MySQL server
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = 'urvi2115'  # MySQL password
app.config['MYSQL_DB'] = 'timezap'  # The name of the database you created

# Initialize MySQL
mysql = MySQL(app)


@app.route('/task.html')
def task():
    # Create a cursor to interact with the database
    cur = mysql.connection.cursor()

    # Retrieve tasks from the database
    cur.execute("SELECT * FROM task")
    tasks = cur.fetchall()  # Fetch all rows from the table

    # Close the cursor
    cur.close()

    return render_template('task.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_id = request.form.get('task_id')
    task_name = request.form.get('task_name')
    priority = request.form.get('priority')

    print(f"task_id: {task_id}, task_name: {task_name}, priority: {priority}")  # Debug print

    # Validate input
    if task_id and task_name:
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Insert task into the database
        cur.execute("INSERT INTO task (task_id, task_name, priority) VALUES (%s, %s, %s)",
                    (task_id, task_name, priority))

        # Commit changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

    return redirect(url_for('task'))


@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id')

    if task_id:
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Delete task from the database
        cur.execute("DELETE FROM task WHERE task_id = %s", [task_id])

        # Commit changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

    return redirect(url_for('task'))

#------------------------------------------------------------------------------------Timer

timer_running = False
timer_time = 25 * 60  # 25 minutes in seconds
start_time = 0
elapsed_time = 0

# Timer Worker
def run_timer():
    global timer_time, elapsed_time, timer_running, start_time
    while timer_running:
        if timer_running:
            # Increment elapsed time
            elapsed_time = time.time() - start_time
            time.sleep(1)

@app.route('/timer.html')
def timer():
    return render_template('timer.html', time_left=timer_time - int(elapsed_time))

@app.route('/start', methods=['POST'])
def start_timer():
    global timer_running, start_time, elapsed_time
    if not timer_running:
        timer_running = True
        start_time = time.time() - elapsed_time  # Start from the elapsed time
        threading.Thread(target=run_timer, daemon=True).start()
    return jsonify({'status': 'started'})

@app.route('/stop', methods=['POST'])
def stop_timer():
    global timer_running
    timer_running = False
    return jsonify({'status': 'stopped'})

@app.route('/reset', methods=['POST'])
def reset_timer():
    global timer_running, elapsed_time
    timer_running = False
    elapsed_time = 0
    return jsonify({'status': 'reset', 'time_left': timer_time})

@app.route('/short_break', methods=['POST'])
def short_break():
    global timer_running, elapsed_time, timer_time
    timer_running = False
    elapsed_time = 0
    timer_time = 5 * 60  # 5 minutes in seconds
    return jsonify({'status': 'short_break', 'time_left': timer_time})

@app.route('/long_break', methods=['POST'])
def long_break():
    global timer_running, elapsed_time, timer_time
    timer_running = False
    elapsed_time = 0
    timer_time = 15 * 60  # 15 minutes in seconds
    return jsonify({'status': 'long_break', 'time_left': timer_time})

if __name__ == '__main__':
    app.run(debug=True)'''

'''from flask import Flask, render_template

app = Flask(__name__ , static_folder='static')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')

# Route for the homepage (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route for landing.html
@app.route('/masonry.html')
def masonry():
    return render_template('masonry.html')

@app.route('/single-post.html')
def single():
    return render_template('single-post.html')

@app.route('/grid.html')
def grid():
    return render_template('grid.html')

@app.route('/blog.html')
def blog():
    return render_template('blog.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)'''


