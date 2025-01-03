import json
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import random


app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config.json', 'r') as f:
    params = json.load(f)['param']

# Configure mail server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = params['gmail-user']
app.config['MAIL_PASSWORD'] = params['gmail-password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Route for login page
@app.route('/')
def login():
    return render_template('login.html')

# Route for login form submission
@app.route('/login', methods=['POST'])
def handle_login():
    email = request.form['email']
    # Generate a random verification code
    verification_code = random.randint(100000, 999999)
    session['email'] = email
    session['verification_code'] = verification_code
    try:
        send_verification_email(email, verification_code)
        flash('A verification code has been sent to your email.', 'success')
    except Exception as e:
        logging.error(f'Failed to send verification email to {email}: {str(e)}')
        flash('Failed to send verification email. Please try again later.', 'danger')
    return redirect(url_for('verify'))

# Route for verification page
@app.route('/verify.html', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        entered_code = request.form['code']
        if 'verification_code' in session and int(entered_code) == session.get('verification_code'):
            flash('Verification successful!', 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Invalid verification code', 'danger')
            return redirect(url_for('verify'))
    return render_template('verify.html')

# Route for the welcome page
@app.route('/welcome.html')
def welcome():
    if 'email' in session:
        return render_template('welcome.html', email=session['email'])
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

# Route for the homepage (index.html)
@app.route('/index.html')
def first():
    return render_template('index.html')

# Route for landing.html
@app.route('/landing.html')
def landing():
    return render_template('landing.html')

# Test email route
@app.route('/test-email')
def test_email():
    test_email = "uv20251@gmail.com"  # Replace with your email to test
    try:
        send_verification_email(test_email, 123456)
        return "Test email sent successfully!"
    except Exception as e:
        logging.error(f'Failed to send test email: {str(e)}')
        return f"Failed to send test email: {str(e)}"

# Function to send a verification email
def send_verification_email(email, code):
    msg = Message(
        'Your Verification Code',
        sender=app.config['MAIL_USERNAME'],  # Use configured email
        recipients=[email]
    )
    msg.body = f"Your verification code is: {code}"
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)

'''import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import random

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

with open('config.json' , 'r') as f :
    params = json.load(f)['param']
# Configure mail server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = params['gmail-user']
app.config['MAIL_PASSWORD'] = params['gmail-password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Dummy user data
users = {
    "test@example.com": "password123"
}


# Route for login page
@app.route('/')
def login():
    return render_template('login.html')




# Route for login form submission

@app.route('/login', methods=['POST'])
def handle_login():
    email = request.form['email']
    password = request.form['password']
    if email in users and users[email] == password:
        verification_code = random.randint(100000, 999999)
        session['email'] = email
        session['verification_code'] = verification_code
        send_verification_email(email, verification_code)
        return redirect(url_for('verify'))
    else:
        flash('Invalid email or password')
        return redirect(url_for('login'))

# Route for verification page
@app.route('/verify.html', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        entered_code = request.form['code']
        if int(entered_code) == session.get('verification_code'):
            return redirect(url_for('welcome'))
        else:
            flash('Invalid verification code')
            return redirect(url_for('verify'))
    return render_template('verify.html')

# Route for the welcome page
@app.route('/welcome.html')
def welcome():
    if 'email' in session:
        return render_template('welcome.html', email=session['email'])
    else:
        return redirect(url_for('login'))

# Route for the homepage (index.html)
@app.route('/index.html')
def first():
    return render_template('index.html')

# Route for landing.html
@app.route('/landing.html')
def landing():
    return render_template('landing.html')

# Function to send a verification email
def send_verification_email(email, code):
    msg = Message('Your Verification Code', sender='your_email@gmail.com', recipients=[email])
    msg.body = f"Your verification code is {code}"
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)










from flask import Flask, render_template

app = Flask(__name__ , static_folder='static')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')

# Route for the homepage (index.html)
@app.route('/index.html')
def first():
    return render_template('index.html')

# Route for landing.html
@app.route('/landing.html')
def landing():
    return render_template('landing.html')

if __name__ == '__main__':
    app.run(debug=True)
'''