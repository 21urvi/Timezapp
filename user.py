import random, string
from flask import session, redirect, url_for, render_template
from database import DatabaseManager


class UserManager:
    def __init__(self):
        self.db = DatabaseManager()

    def generate_captcha(self):
        """Generate a 6-character CAPTCHA"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def login_user(self, request):
        """Handle login logic"""
        msg = ''
        if request.method == 'POST':
            email = request.form['email'].strip().lower()
            password = request.form['password']
            user_captcha = request.form['captcha']
            stored_captcha = session.get('captcha')

            if user_captcha != stored_captcha:
                msg = 'Incorrect CAPTCHA. Try again.'
            else:
                self.db.execute_query('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
                session['user'] = email
                return redirect(url_for('welcome'))

        session['captcha'] = self.generate_captcha()
        return render_template('login.html', captcha=session['captcha'], msg=msg)

    def logout_user(self):
        """Handle logout logic"""
        session.pop('user', None)
        return redirect(url_for('login'))
