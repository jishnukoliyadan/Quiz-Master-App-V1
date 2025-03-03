from quizapp import app

# https://youtu.be/sZl-H6GkHrk?si=BJQdC4LQS9InL68b
@app.template_filter('to_time')
def to_time_filter(value):
    hours = value // 3600
    minutes = (value % 3600) // 60
    seconds = value % 60
    # https://www.geeksforgeeks.org/how-to-pad-a-string-to-a-fixed-length-with-zeros-in-python/
    return f"{hours:0>2} : {minutes:0>2} : {seconds:0>2} sec"


