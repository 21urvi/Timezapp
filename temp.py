from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import random

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

# Configure mail server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

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
@app.route('/verify', methods=['GET', 'POST'])
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


'''from flask import Flask, render_template

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
    app.run(debug=True)'''
