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
    app.run(debug=True)
'''


from flask import Flask, render_template

app = Flask(__name__ , static_folder='static')

'''@app.route('/')
def login():
    return render_template('login.html')

@app.route('/verify.html')
def verify():
    return render_template('verify.html')

@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')'''

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
    app.run(debug=True)