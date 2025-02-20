from flask import request, render_template
from flask import redirect, flash, url_for
from flask import session
from quizapp import app, db
from quizapp.models import User
from datetime import date
# Subject, Chapter
# from quizapp.models import Questions, Quiz, Scores

@app.route('/')
def home():
    return render_template('base_main.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        user_exists = User.query.filter(User.username == username, User.role == 'User').first()
        if user_exists:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        qualification = request.form.get('qualification')
        yyyy, mm, dd = [int(item) for item in request.form.get('dateofbirth').split('-')]
        user = User(username = username, password = password, fullname = fullname,
                    qualification = qualification, dob = date(yyyy, mm, dd))
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registraion is Successful!', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/admin/login', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin_exists = User.query.filter(User.username == username, User.role == 'Admin').first()
        if admin_exists and admin_exists.check_password(password):
            session['admin_id'] = admin_exists.userid
            session['admin_name'] = admin_exists.fullname.split(' ')[0]
            session['admin_role'] = admin_exists.role
            return redirect(url_for('admin_dashboard'))
        flash('Invalid Credentials', 'danger')
    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_exists = User.query.filter(User.username == username, User.role == 'User').first()
        if user_exists and user_exists.check_password(password):
            session['user_id'] = user_exists.userid
            session['user_name'] = user_exists.fullname.split(' ')[0]
            session['user_role'] = user_exists.role
            return redirect(url_for('user_dashboard'))
        flash('Invalid Credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' in session:
        return render_template('admin/dashboard.html')
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))


@app.route('/dashboard')
def user_dashboard():
    if 'user_id' in session:
        return render_template('users/dashboard.html')
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))