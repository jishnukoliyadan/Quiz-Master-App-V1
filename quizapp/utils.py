from quizapp import app, db
from quizapp.models import User, Quiz, Scores
from quizapp.models import Subject, Chapter
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import pandas as pd
import json

# https://youtu.be/sZl-H6GkHrk?si=BJQdC4LQS9InL68b
@app.template_filter('to_time')
def to_time_filter(value):
    hours = value // 3600
    minutes = (value % 3600) // 60
    seconds = value % 60
    # https://www.geeksforgeeks.org/how-to-pad-a-string-to-a-fixed-length-with-zeros-in-python/
    return f"{hours:0>2} : {minutes:0>2} : {seconds:0>2} sec"

def userQuizPerformance(userID, today):
    query = db.session.query(Quiz, Scores).join(Quiz.scores) \
                        .filter(Scores.userid == userID,
                                Quiz.dateofquiz < today) \
                        .order_by(Scores.time_stamp_attempt.desc())
    df = pd.read_sql(query.statement, con = db.engine)[['qname', 'time_stamp_attempt', 'totalscore']]
    fig = px.line(df, x = 'time_stamp_attempt', y = 'totalscore', color = 'qname',
                  title = 'Quiz Performance Over Time<br><sub>Only based on Expired Quizzes</sub>')
    fig.update_traces(mode='markers+lines',
                      hovertemplate = 'Score: %{y}<br>Date: %{x|%d %b}')
    fig.update_layout(xaxis_title = 'Quiz Attempt Time', yaxis_title = 'Total Score',
                      legend = {'title' : 'Quiz Name'}, hovermode = 'x')
    return len(df) > 0, json.dumps(fig, cls = PlotlyJSONEncoder)

def userQuizParticipation(userID):
    query = db.session.query(Quiz, Scores, Subject, Chapter).join(Quiz.scores) \
                            .join(Quiz.chapter).join(Chapter.subject) \
                            .filter(Scores.userid == userID)
    df = pd.read_sql(query.statement, con = db.engine)[['sname', 'cname']]
    df['quiz_attempts'] = 1
    fig = px.sunburst(df, path = ['sname', 'cname'], values = 'quiz_attempts',
                      title = 'Quiz Participation by Subject & Chapter<br><sub>Based on Ongoing & Expired Quizzes</sub>')
    fig.update_traces(hovertemplate = '<b>%{label}</b><br>%{parent}<br>Attempts: %{value}',
                      textinfo = 'label + percent parent')
    fig.update_layout(height = 650)
    return len(df) > 0, json.dumps(fig, cls = PlotlyJSONEncoder)

def Engagement(title, dated = None):
    query = db.session.query(Quiz, Scores, Subject, Chapter, User).join(Quiz.scores)\
                        .join(Quiz.chapter).join(Chapter.subject).join(Scores.user)
    df = pd.read_sql(query.statement, con = db.engine)
    df['quiz_attempts'] = 1
    if dated:
        df = df.query('dateofquiz < @dated').copy(deep = True)
    fig = px.sunburst(df, path = ['sname', 'cname', 'fullname'], values = 'quiz_attempts',
                      color = 'sname', height = 600, title = title,
                      color_discrete_sequence = px.colors.qualitative.Set2)
    fig.update_traces(hovertemplate = '<b>%{label}</b><br>Attempts: %{value}', textinfo = 'label+percent entry')
    return len(df) > 0, json.dumps(fig, cls = PlotlyJSONEncoder)

def QuizPerformance(perform_title):
    query = db.session.query(Scores, Quiz, Chapter, Subject).join(Scores.quiz).join(Quiz.chapter).join(Chapter.subject)
    selected_columns = ['scoreid', 'time_stamp_attempt', 'totalscore', 'quizid', 'userid', 'qname', 'dateofquiz', 'cname', 'sname']
    df = pd.read_sql(query.statement, con = db.engine)[selected_columns]
    df = df.sort_values('time_stamp_attempt', ascending = True) \
                        .drop_duplicates(subset = ['quizid', 'userid'], keep = 'last').reset_index(drop = True)
    quiz_avg_scores = df.groupby(['sname', 'cname', 'qname'])['totalscore'].mean() \
                        .reset_index().sort_values(['sname', 'totalscore'], ascending = [True, False]) \
                        .reset_index(drop = True).rename(columns = {'totalscore' : 'avgScore'})
    fig = px.bar(quiz_avg_scores, x = 'cname', y = 'avgScore',
                 color = 'qname', barmode = 'group', hover_data = ['qname', 'sname'],
                 title = perform_title)
    fig.update_traces(hovertemplate = '<b>Quiz Name: %{customdata[0]}</b><br>' + 
                                      'Chapter: %{x}<br>Subject: %{customdata[1]}<br>Avg.Score: %{y}')
    fig.update_layout(xaxis_title = 'Chapters', yaxis_title = 'Average Score', legend = {'title' : 'Quiz Name'})
    return len(df) > 0, json.dumps(fig, cls = PlotlyJSONEncoder)

def WholeQuizAttemptCount(user_id):
    print(user_id)
    whole_attempt_count = dict()
    wholeQuizAttempt = Scores.query.filter(Scores.userid == user_id)
    for score in wholeQuizAttempt:
        try: whole_attempt_count[score.quizid] += 1
        except: whole_attempt_count[score.quizid] = 1
    return whole_attempt_count