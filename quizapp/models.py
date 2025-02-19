from datetime import datetime
from quizapp import app, db, bcrypt

class User(db.Model):
    userid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), nullable = False, unique = True)
    password = db.Column(db.String(60), nullable = False)
    fullname = db.Column(db.String(60), nullable = False)
    qualification = db.Column(db.String(60), nullable = False)
    dob = db.Column(db.DateTime, nullable = False)
    role = db.Column(db.String(20), nullable = False, default = 'User') # Admin, User

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.fullname}', '{self.qualification}')"

class Subject(db.Model):
    sid = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.Text, nullable = False)
    sname = db.Column(db.String(60), nullable = False, unique = True)

    chapters = db.relationship('Chapter', backref = 'subject', lazy = True)

    def __repr__(self):
        return f"Subject('{self.sname}', '{self.description}')"

class Chapter(db.Model):
    cid = db.Column(db.Integer, primary_key = True)
    cname = db.Column(db.String(60), nullable = False)
    description = db.Column(db.Text, nullable = False)
    subjectid = db.Column(db.Integer, db.ForeignKey('subject.sid'), nullable = False)

    def __repr__(self):
        return f"Chapter('{self.cname}', '{self.description}')"
    
class Quiz(db.Model):
    quizid = db.Column(db.Integer, primary_key = True)
    qname = db.Column(db.String(60), nullable = False)
    dateofquiz = db.Column(db.DateTime, nullable = False)
    timeduration = db.Column(db.Integer, nullable = False)
    remarks = db.Column(db.String(30), nullable = True)
    chapterid = db.Column(db.Integer, db.ForeignKey('chapter.cid'), nullable = False) # (foreign key-chapter)

    def __repr__(self):
        return f"Quiz('{self.chapterid}', '{self.dateofquiz}', '{self.timeduration}')"

class Questions(db.Model):
    qid = db.Column(db.Integer, primary_key = True)
    question_statement = db.Column(db.Text, nullable = False)
    # marks = db.Column(db.Integer, nullable = False)
    option_a = db.Column(db.String(60), nullable = False)
    option_b = db.Column(db.String(60), nullable = False)
    option_c = db.Column(db.String(60), nullable = False)
    option_d = db.Column(db.String(60), nullable = False)
    correct_option = db.Column(db.String(60), nullable = False)
    quizid = db.Column(db.Integer, db.ForeignKey('quiz.quizid'), nullable = False)

    def __repr__(self):
        return f"Questions('{self.quizid}', '{self.question_statement}', '{self.currect_option}')"

class Scores(db.Model):
    scoreid = db.Column(db.Integer, primary_key = True)
    time_stamp_attempt = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)
    totalscore = db.Column(db.Integer, nullable = False)
    quizid = db.Column(db.Integer, db.ForeignKey('quiz.quizid'), nullable = False)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable = False)
    
    def __repr__(self):
        return f"Scores('{self.scoreid}', '{self.userid}', '{self.time_stamp_attempt}', '{self.totalscore}')"

