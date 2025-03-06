from flask import request, render_template
from flask import redirect, flash, url_for
from flask import session
from quizapp import app, db
from quizapp.models import Scores, User, Quiz, Questions
from quizapp.models import Chapter, Subject
from datetime import date
from sqlalchemy import or_
from quizapp import utils

today = date.today()

@app.route('/')
def home():
    session.pop('admin_id', None)
    session.pop('user_id', None)
    return render_template('base_main.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    session.pop('admin_id', None)
    session.pop('user_id', None)
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
    session.pop('admin_id', None)
    session.pop('user_id', None)
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
    session.pop('admin_id', None)
    session.pop('user_id', None)
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

@app.route('/admin/home')
def admin_dashboard():
    session.pop('user_id', None)
    if 'admin_id' in session:
        subjects = Subject.query.all()
        return render_template('admin/dashboard.html', subjects = subjects)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/home')
def user_dashboard():
    session.pop('admin_id', None)
    if 'user_id' in session:
        # https://www.janbasktraining.com/community/sql-server/how-can-i-use-order_by-of-sqlalchemy-to-retrieve-data-in-descending-and-ascending-order
        quizzes = Quiz.query.join(Quiz.question).group_by(Quiz.quizid)
        coming_quizzes = quizzes.filter(Quiz.dateofquiz > today).order_by(Quiz.dateofquiz.asc())
        expired_quizzes = quizzes.filter(Quiz.dateofquiz < today).order_by(Quiz.dateofquiz.desc())
        return render_template('users/dashboard.html', coming_quizzes = coming_quizzes, expired_quizzes = expired_quizzes)
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
            question_exists = Questions.query.filter(Questions.quizid == qid, Questions.question_statement.ilike(f'%{q_statement}%')).first()
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

@app.route('/quiz_details/<int:qid>', methods = ['GET', 'POST'])
def quiz_details(qid):
    if 'user_id' in session:
        quiz = Quiz.query.get_or_404(qid)
        return render_template('users/quiz_details.html', quiz = quiz)
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))

@app.route('/quiz/<int:qid>', methods = ['GET', 'POST'])
def quiz_attempt(qid):
    if 'user_id' in session:
        quiz = Quiz.query.get_or_404(qid)
        if not quiz.dateofquiz.date() >= today:
            flash('The quiz was expired!', 'danger')
            return redirect(url_for('quiz_details', qid = qid))
        questions = quiz.question
        if request.method == "POST":
            user_inputs, qscore = [], 0
            for question in questions:
                user_answer = request.form.get(f'question_{ question.qid }_option')
                user_answer = int(user_answer) if user_answer != None else None
                if user_answer == question.correct_option:
                    qscore += 1
                user_inputs.append(user_answer)
            scores = Scores(**{'userid' : session.get('user_id'),
                               'quizid' : question.quiz.quizid,
                               'totalscore' : qscore})
            scores.store_inputs(user_inputs)
            db.session.add(scores)
            db.session.commit()
            flash('Submission successful. Submit anytime before the deadline; only the final one counts', 'success')
            return redirect(url_for('scores_dashboard'))
        return render_template('users/quiz_attempt.html', questions = questions, quiz = quiz)
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))

@app.route('/scores', methods = ['GET', 'POST'])
def scores_dashboard():
    if 'user_id' in session:
        ongoing_quizzes = Quiz.query.filter(Quiz.dateofquiz > today).order_by(Quiz.dateofquiz.asc())
        expired_quizzes = Quiz.query.filter(Quiz.dateofquiz < today).order_by(Quiz.dateofquiz.asc())
        scores = Scores.query.join(Scores.quiz)\
                                .filter(Scores.userid == session['user_id'], Quiz.dateofquiz < today)\
                                .order_by(Scores.time_stamp_attempt.desc())
        expired_quiz_submitted, attempted_quiz_ids, attempt_count = list(), set(), dict()
        for score in scores:
            if score.quizid not in attempted_quiz_ids:
                expired_quiz_submitted.append(score)
                attempted_quiz_ids.add(score.quizid)
            try: attempt_count[score.quizid] += 1
            except: attempt_count[score.quizid] = 1
        # https://www.w3schools.com/python/ref_list_sort.asp
        expired_quiz_submitted.sort(reverse = False, key = lambda score : score.quiz.dateofquiz)
        unattempted_quizzes = [quiz for quiz in expired_quizzes if quiz.quizid not in attempted_quiz_ids]
        unattempted_quizzes.sort(reverse = True, key = lambda quiz : quiz.dateofquiz)

        return render_template('users/score_dashboard.html', ongoing_quizzes = ongoing_quizzes,
                               expired_quiz_submitted = expired_quiz_submitted,
                               unattempted_quizzes = unattempted_quizzes,
                               attempt_count = attempt_count)
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))

@app.route('/solutions/<int:qid>', methods = ['GET', 'POST'])
def view_solutions(qid):
    if 'user_id' in session:
        quiz = Quiz.query.filter(Quiz.dateofquiz < today, Quiz.quizid == qid).first()
        if not quiz:
            flash('Selected Quiz is still on', 'info')
            return redirect(url_for('scores_dashboard'))
        return render_template('users/view_solutions.html', quiz = quiz)
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))

@app.route('/results/<int:sid>', methods = ['GET', 'POST'])
def view_result(sid):
    if 'user_id' in session:
        score = Scores.query.get_or_404(sid)
        quiz = Quiz.query.filter(Quiz.dateofquiz < today, Quiz.quizid == score.quizid).first()
        if not quiz:
            flash('Selected Quiz is still on', 'info')
            return redirect(url_for('scores_dashboard'))
        attempts = Scores.query.join(Scores.quiz).filter(Scores.userid == score.userid,
                                       Scores.quizid == score.quizid,
                                       Scores.scoreid != sid).order_by(Quiz.dateofquiz.asc())
        return render_template('users/view_result.html', score = score, attempts = attempts)
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))

@app.route('/admin/search', methods = ['GET', 'POST'])
def admin_search():
    if 'admin_id' in session:
        length_= 0
        userQuery, subjectQuery, chapterQuery, quizQuery, questionQuery = [], [], [], [], []
        if request.method == 'POST':
            search_term = request.form.get('search')
            search_pattern = f"%{search_term}%"
            # https://stackoverflow.com/a/7942571
            userQuery = User.query.filter(or_(User.username.ilike(search_pattern),
                                              User.fullname.ilike(search_pattern),
                                              User.qualification.ilike(search_pattern))).all()
            subjectQuery = Subject.query.filter(or_(Subject.sname.ilike(search_pattern),
                                                    Subject.description.ilike(search_pattern))).all()
            chapterQuery = Chapter.query.filter(or_(Chapter.cname.ilike(search_pattern),
                                                    Chapter.description.ilike(search_pattern))).all()
            quizQuery = Quiz.query.filter(or_(Quiz.qname.ilike(search_pattern),
                                              Quiz.remarks.ilike(search_pattern))).all()
            questionQuery = Questions.query.filter(Questions.question_statement.ilike(search_pattern)).all()

            length_ = len(userQuery + subjectQuery + chapterQuery + quizQuery + questionQuery)
            return render_template('admin/search.html', length_= length_, search_term = search_term,
                                   userQuery = userQuery, subjectQuery = subjectQuery,
                                   chapterQuery = chapterQuery, quizQuery = quizQuery,
                                   questionQuery = questionQuery)
        return render_template('admin/search.html', length_ = length_, userQuery = userQuery,
                                    subjectQuery = subjectQuery, chapterQuery = chapterQuery,
                                    quizQuery = quizQuery, questionQuery = questionQuery)
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))

@app.route('/search', methods = ['GET', 'POST'])
def user_search():
    if 'user_id' in session:
        length_= 0
        subjectQuery, chapterQuery, quizQuery = [], [], []
        if request.method == 'POST':
            search_term = request.form.get('search')
            search_pattern = f"%{search_term}%"
            # https://stackoverflow.com/a/7942571
            subjectQuery = Subject.query.filter(or_(Subject.sname.ilike(search_pattern),
                                                    Subject.description.ilike(search_pattern))).all()
            chapterQuery = Chapter.query.filter(or_(Chapter.cname.ilike(search_pattern),
                                                    Chapter.description.ilike(search_pattern))).all()
            quizQuery = Quiz.query.filter(or_(Quiz.qname.ilike(search_pattern),
                                              Quiz.remarks.ilike(search_pattern))).all()
            length_ = len(subjectQuery + chapterQuery + quizQuery)
            return render_template('users/search.html', length_= length_, search_term = search_term,
                                   subjectQuery = subjectQuery,
                                   chapterQuery = chapterQuery, quizQuery = quizQuery)
        return render_template('users/search.html', length_ = length_,
                                    subjectQuery = subjectQuery, chapterQuery = chapterQuery,
                                    quizQuery = quizQuery)
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))

@app.route('/admin/users')
def view_users():
    if 'admin_id' in session:
        users = User.query.filter(User.role == 'User')
        return render_template('admin/view_users.html', users = users)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))

@app.route('/summary', methods = ['GET'])
def user_summary():
    if 'user_id' in session:
        quizExpired, PerformanceJSON = utils.userQuizPerformance(session['user_id'], today)
        participated, ParticipationJSON = utils.userQuizParticipation(session['user_id'])
        return render_template('users/summary_dashboard.html',
                               quizExpired = quizExpired,
                               participated = participated,
                               PerformanceJSON = PerformanceJSON,
                               ParticipationJSON = ParticipationJSON)
    flash('Login to access the page', 'danger')
    return redirect(url_for('login'))

@app.route('/admin/summary', methods = ['GET'])
def admin_summary():
    if 'admin_id' in session:
        all_title = 'User Engagement : Subjects → Chapters → User<br><sub>Based on Ongoing & Expired Quizzes</sub>'
        dated_title = 'User Engagement : Subjects → Chapters → User<br><sub>Only based on Expired Quizzes</sub>'
        perform_title = 'Quiz Performance: Average Scores by Chapter<br><sub>Based on Ongoing & Expired Quizzes</sub>'
        allExists, All_EngagementJSON = utils.Engagement(all_title, dated = False)
        datedExists, Dated_EngagementJSON = utils.Engagement(dated_title, dated = today)
        performExists, PerformanceJSON = utils.QuizPerformance(perform_title)
        return render_template('admin/summary_dashboard.html',
                               allExists = allExists,
                               datedExists = datedExists,
                               All_EngagementJSON = All_EngagementJSON,
                               Dated_EngagementJSON = Dated_EngagementJSON,
                               performExists = performExists,
                               PerformanceJSON = PerformanceJSON)
    flash('Login to access the page', 'danger')
    return redirect(url_for('admin_login'))