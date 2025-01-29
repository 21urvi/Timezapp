from flask import Flask, render_template, request, session, redirect, url_for, flash, send_file
from PIL import Image, ImageDraw, ImageFont
import random
import string
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'


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


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_captcha = request.form['captcha']

        if user_captcha.upper() == session.get('captcha'):
            return "Login Successful!"
        else:
            flash("Incorrect CAPTCHA. Try again.")

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)


'''from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)



# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verify reCAPTCHA
        recaptcha_response = request.form['g-recaptcha-response']
        payload = {
            'secret': '6Lf1HcMqAAAAAAZwyxoayQIfiEkWF6XkEGydcf2h',  # Replace with your actual secret key from Google reCAPTCHA
            'response': recaptcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = response.json()

        if result['success']:
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:  # In production, use hashed passwords!
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials')
        else:
            flash('Please complete the reCAPTCHA')

    return render_template('login.html')


@app.route('/home')
@login_required
def home():
    return "Welcome to your dashboard!"


if __name__ == '__main__':
    with app.app_context():  # Create an application context
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)

'''



'''from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
from flask_mysqldb import MySQL
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'urvi2115'  # Your MySQL password
app.config['MYSQL_DB'] = 'flask_auth'

mysql = MySQL(app)

# Email setup
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_PASSWORD = 'your_email_password'


def send_otp_email(recipient_email, otp):
    """Send OTP to the user's email."""


    try:
        msg = MIMEText(f'Your OTP is: {otp}')
        msg['Subject'] = 'Your OTP Verification Code'
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    email = request.form['email']
    password = request.form['password']

    # Check user credentials
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if user:
        # Generate OTP
        otp = random.randint(100000, 999999)
        cursor.execute("INSERT INTO otps (email, otp_code) VALUES (%s, %s)", (email, otp))
        mysql.connection.commit()
        cursor.close()

        # Send OTP
        send_otp_email(email, otp)

        # Save email in session
        session['email'] = email
        return redirect(url_for('verify'))
    else:
        flash('Invalid email or password.')
        return redirect(url_for('login'))


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        email = session.get('email')
        entered_otp = request.form['code']

        # Check OTP in database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT otp_code FROM otps WHERE email=%s ORDER BY created_at DESC LIMIT 1", (email,))
        stored_otp = cursor.fetchone()

        if stored_otp and int(entered_otp) == stored_otp[0]:
            cursor.execute("DELETE FROM otps WHERE email=%s", (email,))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('welcome'))
        else:
            flash('Invalid OTP. Please try again.')
            return redirect(url_for('verify'))

    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('verify.html')


@app.route('/welcome.html')
def welcome():
    return "<h1>Welcome! You have successfully logged in.</h1>"


if __name__ == '__main__':
    app.run(debug=True)'''

'''from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import bcrypt  # For hashing passwords
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'urvi2115'  # Change this to your actual MySQL password
app.config['MYSQL_DB'] = 'timezap'

mysql = MySQL(app)


# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# Function to verify passwords
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)  # Hash the password

        # Store user in the database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO login (email, password) VALUES (%s, %s)", (email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT password FROM login WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            stored_password = user[0]
            if password == stored_password:  # Use password hashing in production!
                session['email'] = email
                return redirect(url_for('home'))
            else:
                flash('Invalid password.')
        else:
            flash('User not found.')

    return render_template('login.html')

@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return f"Welcome, {session['email']}!"


if __name__ == '__main__':
    app.run(debug=True)'''

'''timer_running = False
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

@app.route('/')
def open_py_file() :
    call(["python","list.py"])
    return render_template(open_py_file())'''

