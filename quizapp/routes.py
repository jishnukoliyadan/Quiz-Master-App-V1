from flask import request, render_template
from flask import redirect, flash, url_for
from flask import session
from quizapp import app, db
from quizapp.models import User, Quiz, Questions
from quizapp.models import Chapter, Subject
from datetime import date
# Scores

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
    session.pop('user_id', None)
    if 'admin_id' in session:
        subjects = Subject.query.all()
        return render_template('admin/dashboard.html', subjects = subjects)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))


@app.route('/dashboard')
def user_dashboard():
    session.pop('admin_id', None)
    if 'user_id' in session:
        return render_template('users/dashboard.html')
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))

@app.route('/admin/add_subject', methods = ['GET', 'POST'])
def add_subject():
    if 'admin_id' in session:
        if request.method == 'POST':
            sname = request.form.get('name')
            description = request.form.get('description')
            # https://stackoverflow.com/a/54672057
            subject_exists = Subject.query.filter(Subject.sname.ilike(f'%{sname}%')).first()
            if not subject_exists:
                subject = Subject(sname = sname, description = description)
                db.session.add(subject)
                db.session.commit()
                flash('New subject added!', 'success')
                return redirect(url_for('admin_dashboard'))
            flash('Subject already exists!', 'danger')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/add_subject.html')
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))
    
@app.route('/admin/add_chapter/<int:sid>', methods = ['GET', 'POST'])
def add_chapter(sid):
    if 'admin_id' in session:
        if request.method == 'POST':
            cname = request.form.get('name')
            description = request.form.get('description')
            chapter = Chapter(cname = cname, description = description, subjectid = sid)
            db.session.add(chapter)
            db.session.commit()
            flash(f'Chapter added to {chapter.subject.sname}!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/add_chapter.html')
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/delete_chapter/<int:cid>', methods = ['POST'])
def delete_chapter(cid):
    if 'admin_id' in session:
        chapter = Chapter.query.get_or_404(cid)
        db.session.delete(chapter)
        db.session.commit()
        flash('Chapter deleted!', 'success')
        return redirect(url_for('admin_dashboard'))
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/quiz', methods = ['GET', 'POST'])
def manage_quizzes():
    if 'admin_id' in session:
        quizz = Quiz.query.all()
        return render_template('admin/quiz.html', quizzes=quizz )
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/add_question/<int:qid>', methods = ['GET', 'POST'])
def add_question(qid):
    if 'admin_id' in session:
        quiz = Quiz.query.filter(Quiz.quizid == qid).first()
        if request.method == 'POST':
            q_statement = request.form.get('q_statement')
            question_exists = Questions.query.filter(Questions.question_statement.ilike(f'%{q_statement}%')).first()
            if question_exists:
                flash(f'Question exists in {quiz.qname}!', 'danger')
                return redirect(url_for('manage_quizzes'))
            question = Questions(**{'question_statement' : q_statement,
                                    'option_a' : request.form.get('option_1'),
                                    'option_b' : request.form.get('option_2'),
                                    'option_c' : request.form.get('option_3'),
                                    'option_d' : request.form.get('option_4'),
                                    'correct_option' : int(request.form.get('correctOption')),
                                    'quizid' : quiz.quizid})
            db.session.add(question)
            db.session.commit()
            flash(f'New question added to {quiz.qname}!', 'success')
            return redirect(url_for('manage_quizzes'))
        return render_template('admin/add_question.html', quiz = quiz)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))


@app.route('/admin/delete_question/<int:qid>', methods = ['POST'])
def delete_question(qid):
    if 'admin_id' in session:
        question = Questions.query.get_or_404(qid)
        qname = question.quiz.qname
        db.session.delete(question)
        db.session.commit()
        flash(f'Deleted question from {qname}!', 'success')
        return redirect(url_for('manage_quizzes'))
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/delete_subject/<int:sid>', methods = ['POST'])
def delete_subject(sid):
    if 'admin_id' in session:
        subject = Subject.query.get_or_404(sid)
        sname = subject.sname
        db.session.delete(subject)
        db.session.commit()
        flash(f'Deleted subject {sname}!', 'success')
        return redirect(url_for('admin_dashboard'))
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/edit_question/<int:qid>', methods = ['GET', 'POST'])
def edit_question(qid):
    if 'admin_id' in session:
        question = Questions.query.filter(Questions.qid == qid).first()
        if request.method == 'POST':
            update_data = {'question_statement' : request.form.get('q_statement'),
                           'option_a' : request.form.get('option_1'),
                           'option_b' : request.form.get('option_2'),
                           'option_c' : request.form.get('option_3'),
                           'option_d' : request.form.get('option_4'),
                           'correct_option' : int(request.form.get('correctOption')),
                           'quizid' : question.quiz.quizid}
            
            # https://medium.com/@s.azad4/modifying-python-objects-within-the-sqlalchemy-framework-7b6c8dd71ab3
            for key, value in update_data.items():
                setattr(question, key, value)
            db.session.commit()

            flash(f'Question Updated!', 'success')
            return redirect(url_for('view_question', qid = question.qid))
        return render_template('admin/edit_question.html', question = question)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/view_question/<int:qid>', methods = ['GET', 'POST'])
def view_question(qid):
    if 'admin_id' in session:
        question = Questions.query.get_or_404(qid)
        return render_template('admin/view_question.html', question = question)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/edit_subject/<int:sid>', methods = ['GET', 'POST'])
def edit_subject(sid):
    if 'admin_id' in session:
        subject = Subject.query.filter(Subject.sid == sid).first()
        if request.method == 'POST':
            update_data = {'sname' : request.form.get('sname'),
                           'description' : request.form.get('description')}
            for key, value in update_data.items():
                setattr(subject, key, value)
            db.session.commit()
            flash(f'Subject {subject.sname} updated!', 'success')
            return redirect(url_for('view_subject', sid = subject.sid))
        return render_template('admin/edit_subject.html', subject = subject)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))


@app.route('/admin/edit_chapter/<int:cid>', methods = ['GET', 'POST'])
def edit_chapter(cid):
    if 'admin_id' in session:
        chapter = Chapter.query.filter(Chapter.cid == cid).first()
        if request.method == 'POST':
            update_data = {'cname' : request.form.get('cname'),
                           'description' : request.form.get('description')}
            for key, value in update_data.items():
                setattr(chapter, key, value)
            db.session.commit()
            flash(f'Chapter "{chapter.cname}" updated!', 'success')
            return redirect(url_for('view_chapter', cid = chapter.cid))
        return render_template('admin/edit_chapter.html', chapter = chapter)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/add_quiz', methods = ['GET', 'POST'])
def add_quiz():
    if 'admin_id' in session:
        subjects = Subject.query.all()
        if request.method == 'POST':
            yyyy, mm, dd = [int(item) for item in request.form.get('dateofquiz').split('-')]
            
            quiz = Quiz(**{'qname' : request.form.get('qname'),
                           'dateofquiz' : date(yyyy, mm, dd),
                           'timeduration' : int(request.form.get('tDuration'))*60,
                           'remarks' : request.form.get('remarks'),
                           'chapterid' : int(request.form.get('chapterID'))})
            db.session.add(quiz)
            db.session.commit()
            flash(f'Added new Quiz to {quiz.chapter.cname}!', 'success')
            return redirect(url_for('manage_quizzes'))
        return render_template('admin/add_quiz.html', subjects = subjects)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/view_quiz/<int:qid>', methods = ['GET', 'POST'])
def view_quiz(qid):
    if 'admin_id' in session:
        quiz = Quiz.query.get_or_404(qid)
        return render_template('admin/view_quiz.html', quiz = quiz)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/edit_quiz/<int:qid>', methods = ['GET', 'POST'])
def edit_quiz(qid):
    if 'admin_id' in session:
        quiz = Quiz.query.filter(Quiz.quizid == qid).first()
        if request.method == 'POST':
            yyyy, mm, dd = [int(item) for item in request.form.get('qdate').split('-')]
            update_data = {'qname' : request.form.get('qname'),
                           'timeduration' : int(float(request.form.get('tDuration'))) * 60,
                           'dateofquiz' : date(yyyy, mm, dd),
                           'remarks' : request.form.get('remarks')}
            for key, value in update_data.items():
                setattr(quiz, key, value)
            db.session.commit()
            flash(f'Quiz data updated!', 'success')
            return redirect(url_for('view_quiz', qid = qid))
        return render_template('admin/edit_quiz.html', quiz = quiz)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/delete_quiz/<int:qid>', methods = ['GET', 'POST'])
def delete_quiz(qid):
    print('jishnu')
    if 'admin_id' in session:
        quiz = Quiz.query.get_or_404(qid)
        qname = quiz.qname
        db.session.delete(quiz)
        db.session.commit()
        flash(f'Deleted Quiz "{qname}"!', 'success')
        return redirect(url_for('manage_quizzes'))
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/view_subject/<int:sid>', methods = ['GET', 'POST'])
def view_subject(sid):
    if 'admin_id' in session:
        subject = Subject.query.get_or_404(sid)
        return render_template('admin/view_subject.html', subject = subject)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/view_chapter/<int:cid>', methods = ['GET', 'POST'])
def view_chapter(cid):
    if 'admin_id' in session:
        chapter = Chapter.query.get_or_404(cid)
        return render_template('admin/view_chapter.html', chapter = chapter)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))