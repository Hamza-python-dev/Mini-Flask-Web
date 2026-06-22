from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
import os

auth = Blueprint('auth', __name__)

ADMIN_USERNAME = None  # set via app config or import from os.getenv
ADMIN_PASSWORD = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            session['logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        return render_template('login.html', error="Wrong username or password!")
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))