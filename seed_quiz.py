import os
from dotenv import load_dotenv
from quizapp import db, DB_NAME
from quizapp.models import User, Subject, Chapter
from quizapp.models import Questions, Quiz, Scores
from datetime import date

if os.path.exists(f'./instance/{DB_NAME}'):
    os.remove(f'./instance/{DB_NAME}')
db.create_all()

load_dotenv()

users_data = [
    {'username' : 'jane@doe',
     'password' : '12345',
     'fullname' : 'Jane Doe',
     'qualification' : 'BSc',
     'dob' : date(1996, 2, 15),
     },
     {'username' : 'ram@raj',
     'password' : '23456',
     'fullname' : 'Ram Raj',
     'qualification' : 'Diploma',
     'dob' : date(1998, 12, 19),
     },
     {'username' : 'josh@jain',
     'password' : '34567',
     'fullname' : 'Josh Jain',
     'qualification' : 'BS',
     'dob' : date(1997, 5, 25),
     }]

subject_data = [
    {'sname' : 'Mathematics',
     'description' : 'Study of numbers, logic and patters'},
    {'sname' : 'Physics',
     'description' : 'Study of motion, energy, matter'},
    {'sname' : 'Computer Science',
     'description' : 'Study of computation, information, and automation'}]

chapter_data = [
    {'cname' : 'Algebraic Expressions',
     'description' : 'Symbols, equations, solve',
     'subjectid' : 1,
     },
    {'cname' : 'Force',
     'description' : 'A push or pull on an object.',
     'subjectid' : 2,
     },
    {'cname' : 'Programming Languages',
     'description' : 'A code system for computers to run.',
     'subjectid' : 3,
     },
    {'cname' : 'Junior Maths',
     'description' : 'Class 5 Maths',
     'subjectid' : 1,
     }]

quiz_data = [
    {'qname' : 'Quiz 1',
     'dateofquiz' : date(2025, 3, 1),
     'timeduration' : 3*60,
     'chapterid' : 1,
     },
    {'qname' : 'Quiz 2',
     'dateofquiz' : date(2025, 3, 20),
     'timeduration' : 3*60,
     'chapterid' : 2,
     },
    {'qname' : 'Quiz 3',
     'dateofquiz' : date(2025, 4, 20),
     'timeduration' : 3*60,
     'chapterid' : 2,
     },
    {'qname' : 'Quiz 4',
     'dateofquiz' : date(2025, 5, 20),
     'timeduration' : 3*60,
     'chapterid' : 1,
     },
    {'qname' : 'Quiz 5',
     'dateofquiz' : date(2025, 5, 20),
     'timeduration' : 3*60,
     'chapterid' : 3,
     },
    {'qname' : 'Quiz 6',
     'dateofquiz' : date(2025, 6, 20),
     'timeduration' : 3*60,
     'chapterid' : 4,
     }]

questions_data = [
    # https://byjus.com/maths/class-8-maths-chapter-9-algebraic-expression-and-identities-mcqs/
    {'question_statement' : 'The product of 5x and 3y is:',
     'option_a' : 'xy',
     'option_b' : '2xy',
     'option_c' : '5xy',
     'option_d' : '15xy',
     'correct_option' : 4,
     'quizid' : 1,
     },
    {'question_statement' : 'The product of 6x and -11x is:',
     'option_a' : '66x²',
     'option_b' : '-66x²',
     'option_c' : 'x²',
     'option_d' : '-x²',
     'correct_option' : 1,
     'quizid' : 1,
     },
    {'question_statement' : 'The product of 4x and 0 is:',
     'option_a' : '4x',
     'option_b' : '4',
     'option_c' : '0',
     'option_d' : 'None of the above',
     'correct_option' : 3,
     'quizid' : 1,
     },
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
    {'userid' : '1' , 'quizid' : '1', 'totalscore' : '2'},
    {'userid' : '2' , 'quizid' : '2', 'totalscore' : '3'}]

admin = User(**{'username' : os.getenv('ADMIN_USERNAME'),
                'password' : os.getenv('ADMIN_PASSWORD'),
                'fullname' : 'Admin',
                'qualification' : '',
                'dob' : date(1990, 1, 1),
                'role' : 'Admin'})
admin.set_password(os.getenv('ADMIN_PASSWORD'))
db.session.add(admin)

for users in users_data:
    user = User(**users)
    user.set_password(users.get('password'))
    db.session.add(user)

for subject_ in subject_data:
    subject = Subject(**subject_)
    db.session.add(subject)

for chapter_ in chapter_data:
    chapter = Chapter(**chapter_)
    db.session.add(chapter)

for quiz_ in quiz_data:
    quiz = Quiz(**quiz_)
    db.session.add(quiz)

for questions in questions_data:
    question = Questions(**questions)
    db.session.add(question)

for scores in scores_data:
    score = Scores(**scores)
    db.session.add(score)

db.session.commit()