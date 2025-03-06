import os
import json
from datetime import date, datetime
from dotenv import load_dotenv
from quizapp import db, DB_NAME
from quizapp.models import User, Subject, Chapter
from quizapp.models import Quiz, Questions, Scores

def seed_db():
    existed = check_db_existance(DB_NAME)
    if not existed:
        add_admin_to_db()
        add_sample_users()
        add_sample_subjects()
        add_sample_chapters()
        add_sample_quizzes()
        add_sample_questions(questions_data)
        simulate_quiz_attempts(scores_data)

def check_db_existance(db_name):
    dbExist = os.path.exists(f'./instance/{db_name}')
    if not dbExist:
        db.create_all()
        return False
    return True

def add_admin_to_db():
    load_dotenv()
    admin = User(**{'username' : os.getenv('ADMIN_USERNAME'),
                    'password' : os.getenv('ADMIN_PASSWORD'),
                    'fullname' : 'Admin',
                    'qualification' : 'Super Admin',
                    'dob' : date(1990, 1, 1),
                    'role' : 'Admin'})
    admin.set_password(os.getenv('ADMIN_PASSWORD'))
    db.session.add(admin)
    db.session.commit()
    print("Admin created!")

def add_sample_users():
    users_data = [{'username' : 'jane@doe', 'password' : '12345', 'fullname' : 'Jane Doe',
                   'qualification' : 'BSc', 'dob' : date(1996, 2, 15)},
                  {'username' : 'ram@raj', 'password' : '12345', 'fullname' : 'Ram Raj',
                   'qualification' : 'Diploma', 'dob' : date(1998, 12, 19)},
                  {'username' : 'josh@jain', 'password' : '12345', 'fullname' : 'Josh Jain',
                   'qualification' : 'BS', 'dob' : date(1997, 5, 25)}]
    for users in users_data:
        user = User(**users)
        user.set_password(users.get('password'))
        db.session.add(user)
    db.session.commit()
    print("Sample Users created!")

def add_sample_subjects():
    subject_data = [{'sname' : 'Mathematics', 'description' : 'Study of numbers, logic and patters'},
                    {'sname' : 'Physics', 'description' : 'Study of motion, energy, matter'},
                    {'sname' : 'Computer Science', 'description' : 'Study of computation, information, and automation'}]
    for subject_ in subject_data:
        subject = Subject(**subject_)
        db.session.add(subject)
    db.session.commit()
    print("Sample Subjects created!")

def add_sample_chapters():
    chapter_data = [{'cname' : 'Algebraic Expressions', 'description' : 'Symbols, equations, solve', 'subjectid' : 1},
                    {'cname' : 'Force', 'description' : 'A push or pull on an object.', 'subjectid' : 2},
                    {'cname' : 'Programming Languages', 'description' : 'A code system for computers to run.', 'subjectid' : 3},
                    {'cname' : 'Junior Maths', 'description' : 'Class 5 Maths', 'subjectid' : 1}]
    for chapter_ in chapter_data:
        chapter = Chapter(**chapter_)
        db.session.add(chapter)
    db.session.commit()
    print("Sample Chapters created!")

def add_sample_quizzes():
    quiz_data = [{'qname' : 'Quiz 1', 'dateofquiz' : date(2025, 3, 1), 'timeduration' : 1*60, 'chapterid' : 1},
                 {'qname' : 'Quiz 2', 'dateofquiz' : date(2025, 3, 20), 'timeduration' : 1*60, 'chapterid' : 2},
                 {'qname' : 'Quiz 3', 'dateofquiz' : date(2025, 4, 20), 'timeduration' : 1*60, 'chapterid' : 2},
                 {'qname' : 'Quiz 4', 'dateofquiz' : date(2025, 5, 20), 'timeduration' : 1*60, 'chapterid' : 1},
                 {'qname' : 'Quiz 5', 'dateofquiz' : date(2025, 5, 20), 'timeduration' : 1*60, 'chapterid' : 3},
                 {'qname' : 'Quiz 6', 'dateofquiz' : date(2025, 6, 20), 'timeduration' : 1*60, 'chapterid' : 4}]
    for quiz_ in quiz_data:
        quiz = Quiz(**quiz_)
        db.session.add(quiz)
    db.session.commit()
    print("Sample Quizzes created!")

def add_sample_questions(sample_questions):
    for questions in sample_questions:
        question = Questions(**questions)
        db.session.add(question)
    db.session.commit()
    print("Sample Questions created!")

def simulate_quiz_attempts(score_simulations):
    for scores in score_simulations:
        score = Scores(**scores)
        db.session.add(score)
    db.session.commit()
    print("Simulated Quizzes!")

questions_data = [
    # https://byjus.com/maths/class-8-maths-chapter-9-algebraic-expression-and-identities-mcqs/
    {'question_statement' : 'The product of 5x and 3y is:',
     'option_a' : 'xy',
     'option_b' : '2xy',
     'option_c' : '5xy',
     'option_d' : '15xy',
     'correct_option' : 4,
     'quizid' : 1},
    {'question_statement' : 'The product of 6x and -11x is:',
     'option_a' : '66x²',
     'option_b' : '-66x²',
     'option_c' : 'x²',
     'option_d' : '-x²',
     'correct_option' : 2,
     'quizid' : 1},
    {'question_statement' : 'The product of 4x and 0 is:',
     'option_a' : '4x',
     'option_b' : '4',
     'option_c' : '0',
     'option_d' : 'None of the above',
     'correct_option' : 3,
     'quizid' : 1},
    # https://icsehelp.com/icse-physics-class-10-force-mcq-type-questions/
    {'question_statement' : 'A nut is opened by a wrench of length 10cm. If the least force required is 5.0N, find the moment of force needed to turn the nut.',
     'option_a' : '0.5 Nm',
     'option_b' : '50 Nm',
     'option_c' : '2 Nm',
     'option_d' : 'None of the above',
     'correct_option' : 1, # Moment Force = F * r = 5 * 0.1 = 0.5 Nm
     'quizid' : 2,
     },
    {'question_statement' : 'The turning effect produced in a rigid body around a fixed point by the application of force is called;',
     'option_a' : 'Turning force',
     'option_b' : 'Movement of force',
     'option_c' : 'Moment of couple',
     'option_d' : 'None of these',
     'correct_option' : 2,
     'quizid' : 2,
     },
    {'question_statement' : 'The unit of moment of force in Sl system is:',
     'option_a' : 'Nm',
     'option_b' : 'dyne cm',
     'option_c' : 'dyne m',
     'option_d' : 'N cm',
     'correct_option' : 1,
     'quizid' : 2,
     },
    # https://testbook.com/objective-questions/mcq-on-force-and-mass--5eea6a1339140f30f369ef47
    {'question_statement' : 'Which of the following is NOT a force ?',
     'option_a' : 'Tension',
     'option_b' : 'Normal',
     'option_c' : 'Mass',
     'option_d' : 'Weight',
     'correct_option' : 3,
     'quizid' : 3,
     },
    {'question_statement' : 'What is the SI unit of thrust',
     'option_a' : 'Newton metre (N m)',
     'option_b' : 'Newton per metre (N / m)',
     'option_c' : 'Pascal (Pa)',
     'option_d' : 'Newton (N)',
     'correct_option' : 4,
     'quizid' : 3,
     },
    {'question_statement' : 'What is the coefficient of x in the expresstion 4x + 3y ?',
     'option_a' : '1',
     'option_b' : '2',
     'option_c' : '3',
     'option_d' : '4',
     'correct_option' : 4,
     'quizid' : 4,
     },
    # https://www.studiestoday.com/mcq-mathematics-cbse-class-5-mathematics-introduction-algebra-mcqs-312093.html
    {'question_statement' : 'a = 9, b = 3 the a ÷ b =?',
     'option_a' : '3',
     'option_b' : '9',
     'option_c' : '12',
     'option_d' : '0',
     'correct_option' : 1,
     'quizid' : 4,
     },
    {'question_statement' : 'x=5, y=7 then x+y=?',
     'option_a' : '12',
     'option_b' : '-2',
     'option_c' : '13',
     'option_d' : '35',
     'correct_option' : 1,
     'quizid' : 4,
     },
    # https://testbook.com/objective-questions/mcq-on-programming-and-data-structure--5eea6a1139140f30f369eb7c
    {'question_statement' : 'Which of the following is NOT a programming language?',
     'option_a' : 'C++',
     'option_b' : 'Java',
     'option_c' : 'Python',
     'option_d' : 'Linux',
     'correct_option' : 4,
     'quizid' : 5,
     },
    # https://www.freshersnow.com/computer-programming-mcqs-and-answers-with-explanation/
    {'question_statement' : 'Which operator is used for exponentiation in most programming languages?',
     'option_a' : '^',
     'option_b' : '*',
     'option_c' : '%',
     'option_d' : '**',
     'correct_option' : 4,
     'quizid' : 5,
     },
    # https://www.studiestoday.com/mcq-mathematics-cbse-class-5-mathematics-mcqs-299615.html
    {'question_statement' : '___ ÷ 1000 = 7.531',
     'option_a' : '7531',
     'option_b' : '75.31',
     'option_c' : '753.1',
     'option_d' : '0.7531',
     'correct_option' : 1,
     'quizid' : 6,
     },
    {'question_statement' : '8.01 X ___ = 80100',
     'option_a' : '10000',
     'option_b' : '100',
     'option_c' : '1000',
     'option_d' : '10',
     'correct_option' : 1,
     'quizid' : 6,
     }]

scores_data = [
    {'userid' : 2 , 'quizid' : 1, 'totalscore' : 2, 'user_input' : json.dumps([4, None, 3]), 'time_stamp_attempt' : datetime(2025, 3, 1, 10, 30, 45, 123456)},
    {'userid' : 2 , 'quizid' : 1, 'totalscore' : 2, 'user_input' : json.dumps([None, 2, 3]), 'time_stamp_attempt' : datetime(2025, 3, 2, 20, 30, 45, 123456)},
    {'userid' : 2 , 'quizid' : 1, 'totalscore' : 0, 'user_input' : json.dumps([None, None, None]), 'time_stamp_attempt' : datetime(2025, 3, 4, 13, 30, 45, 123456)},
    {'userid' : 2 , 'quizid' : 1, 'totalscore' : 2, 'user_input' : json.dumps([4, 2, None]), 'time_stamp_attempt' : datetime(2025, 3, 5, 13, 30, 45, 123456)},
    {'userid' : 2 , 'quizid' : 1, 'totalscore' : 3, 'user_input' : json.dumps([4, 2, 3]), 'time_stamp_attempt' : datetime(2025, 3, 6, 18, 30, 45, 123456)},
    
    {'userid' : 2 , 'quizid' : 2, 'totalscore' : 2, 'user_input' : json.dumps([1, 2, None]), 'time_stamp_attempt' : datetime(2025, 3, 5, 21, 30, 45, 123456)},
    {'userid' : 2 , 'quizid' : 2, 'totalscore' : 1, 'user_input' : json.dumps([2, 4, 1]), 'time_stamp_attempt' : datetime(2025, 3, 6, 9, 30, 45, 123456)},
    {'userid' : 2 , 'quizid' : 2, 'totalscore' : 3, 'user_input' : json.dumps([1, 2, 1]), 'time_stamp_attempt' : datetime(2025, 3, 6, 20, 30, 45, 123456)},

    {'userid' : 2 , 'quizid' : 5, 'totalscore' : 1, 'user_input' : json.dumps([1, 4]), 'time_stamp_attempt' : datetime(2025, 3, 4, 20, 30, 45, 123456)},
    {'userid' : 2 , 'quizid' : 5, 'totalscore' : 2, 'user_input' : json.dumps([4, 4]), 'time_stamp_attempt' : datetime(2025, 3, 6, 20, 30, 45, 123456)},
    
    {'userid' : 2 , 'quizid' : 6, 'totalscore' : 0, 'user_input' : json.dumps([3, 2]), 'time_stamp_attempt' : datetime(2025, 3, 5, 15, 30, 45, 123456)},
    {'userid' : 2 , 'quizid' : 6, 'totalscore' : 2, 'user_input' : json.dumps([1, 1]), 'time_stamp_attempt' : datetime(2025, 3, 6, 20, 30, 45, 123456)},
    
    {'userid' : 3 , 'quizid' : 3, 'totalscore' : 1, 'user_input' : json.dumps([3, 2]), 'time_stamp_attempt' : datetime(2025, 3, 4, 15, 30, 45, 123456)},
    {'userid' : 3 , 'quizid' : 3, 'totalscore' : 0, 'user_input' : json.dumps([1, 3]), 'time_stamp_attempt' : datetime(2025, 3, 5, 23, 30, 45, 123456)},
    {'userid' : 3 , 'quizid' : 3, 'totalscore' : 2, 'user_input' : json.dumps([3, 4]), 'time_stamp_attempt' : datetime(2025, 3, 6, 20, 30, 45, 123456)},
    
    {'userid' : 3 , 'quizid' : 4, 'totalscore' : 2, 'user_input' : json.dumps([4, 1, 2]), 'time_stamp_attempt' : datetime(2025, 3, 3, 20, 30, 45, 123456)},
    {'userid' : 3 , 'quizid' : 4, 'totalscore' : 1, 'user_input' : json.dumps([2, 2, 1]), 'time_stamp_attempt' : datetime(2025, 3, 5, 15, 30, 45, 123456)},
    {'userid' : 3 , 'quizid' : 4, 'totalscore' : 2, 'user_input' : json.dumps([3, 1, 1]), 'time_stamp_attempt' : datetime(2025, 3, 6, 23, 30, 45, 123456)},
    
    {'userid' : 3 , 'quizid' : 1, 'totalscore' : 3, 'user_input' : json.dumps([4, 2, 3]), 'time_stamp_attempt' : datetime(2025, 3, 5, 5, 30, 45, 123456)},
    {'userid' : 3 , 'quizid' : 1, 'totalscore' : 2, 'user_input' : json.dumps([4, 2, None]), 'time_stamp_attempt' : datetime(2025, 3, 6, 8, 30, 45, 123456)},
    
    {'userid' : 4 , 'quizid' : 2, 'totalscore' : 1, 'user_input' : json.dumps([1, 2, 1]), 'time_stamp_attempt' : datetime(2025, 3, 5, 5, 30, 45, 123456)},
    {'userid' : 4 , 'quizid' : 2, 'totalscore' : 3, 'user_input' : json.dumps([1, 2, 1]), 'time_stamp_attempt' : datetime(2025, 3, 6, 11, 30, 45, 123456)},
    {'userid' : 4 , 'quizid' : 2, 'totalscore' : 0, 'user_input' : json.dumps([None, None, None]), 'time_stamp_attempt' : datetime(2025, 3, 6, 17, 30, 45, 123456)},
    
    {'userid' : 4 , 'quizid' : 4, 'totalscore' : 1, 'user_input' : json.dumps([4, 3, 2]), 'time_stamp_attempt' : datetime(2025, 3, 4, 14, 30, 45, 123456)},
    {'userid' : 4 , 'quizid' : 4, 'totalscore' : 3, 'user_input' : json.dumps([4, 1, 1]), 'time_stamp_attempt' : datetime(2025, 3, 6, 19, 30, 45, 123456)},
    
    {'userid' : 4 , 'quizid' : 5, 'totalscore' : 2, 'user_input' : json.dumps([4, 4]), 'time_stamp_attempt' : datetime(2025, 3, 5, 10, 30, 45, 123456)},
    {'userid' : 4 , 'quizid' : 5, 'totalscore' : 0, 'user_input' : json.dumps([None, None]), 'time_stamp_attempt' : datetime(2025, 3, 6, 16, 30, 45, 123456)},
    {'userid' : 4 , 'quizid' : 5, 'totalscore' : 2, 'user_input' : json.dumps([4, 4]), 'time_stamp_attempt' : datetime(2025, 3, 6, 23, 30, 45, 123456)}
    ]