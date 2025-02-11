'''from flask import Flask, render_template, request, redirect, url_for, session
import random, string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        user_captcha = request.form['captcha']
        stored_captcha = session.get('captcha')

        if user_captcha == stored_captcha:
            session['user'] = email
            return redirect(url_for('welcome'))  # Redirect to welcome page

    session['captcha'] = generate_captcha()  # Generate new CAPTCHA on reload
    return render_template('login.html', captcha=session['captcha'])

@app.route('/welcome')
def welcome():
    if 'user' in session:
        return render_template('welcome.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)'''

from flask import Flask, render_template, request, redirect, url_for, session
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

@app.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('welcome'))

    session['captcha'] = generate_captcha()  # Refresh CAPTCHA
    return render_template('login.html', captcha=session['captcha'], msg=msg)

@app.route('/welcome')
def welcome():
    if 'user' in session:
        return render_template('welcome.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
