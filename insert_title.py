from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/insert_title')
def insert_title():
    #title=request.form['title']
    title="SAMPLE QUIZ"
    if title:
        return render_template("general_options.html", title=title)
    
    else:
        return render_template("home_instructor.html")



@app.route('/insert_GO', methods=['POST'])
def insert_GO():
    #random_ques=request.form['random_questions']
    #random_ans=request.form['random_answers']
    #max_time=request.form['time']
    
    #PUT VALUES IN DATABSE
        
    return render_template("custom_messages.html")

@app.route('/congrats', methods=['POST'])
def congrats():
    #random_ques=request.form['random_questions']
    #random_ans=request.form['random_answers']
    #max_time=request.form['time']
    
    #PUT VALUES IN DATABSE
        
    return render_template("congrats.html")

@app.route('/assessments')
def assessments():
    return render_template('assessments.html')

@app.route('/add_question_basic')
def add_question():
    return render_template('add_question_basic.html')

@app.route('/insert_question_text', methods=['POST'])
def insert_question_text():
    type=request.form['type']
    if(type=='MCQ'):
        return render_template('insert_question_text.html')
    
@app.route('/insert_choices', methods=['POST'])
def insert_choices():
    return render_template('insert_choices.html')



app.run(debug=True)