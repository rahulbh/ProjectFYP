from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from wtforms import Form, RadioField
import os
from wtforms import TextField, validators, PasswordField, TextAreaField, HiddenField, SubmitField
from db_init_final import QnA, db, load_db, MCQMCMR
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
#from insert_QnA_data import insert_MCQ_QnA

# Flask: Initialize
app = Flask(__name__)
 
# Flask-SQLAlchemy: Initialize
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testuser:test123@localhost:5432/testdb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testuser:xxxx@localhost:5432/testdb'
db.init_app(app)   # Bind SQLAlchemy to this Flask app
 
# Create the database tables and records inside a temporary test context
with app.test_request_context():
    load_db(db)
    
data=QnA()


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

class QuestionDesc(Form):
        desc = TextAreaField('desc', [validators.Required("Please enter Description.")])
        counter = TextField('counter')
        group = TextField('group')
        submit = SubmitField('submit')
        
type=0
        
@app.route('/insert_question_text', methods=['POST'])
def insert_question_text():
    global type
    type=request.form['type']
    form=QuestionDesc()
    if(type=='MCQ' or type=='MCMR'):
        return render_template('insert_question_text.html', form=form)
    elif(type=='FIB'):
        return render_template('FIB_insert_question_text.html', form=form)
    else:
        return render_template('SA_insert_question_text.html', form=form)
        
    
param_count=0
hasParam=0
acounter=0

@app.route('/check_param_type', methods=['POST'])
def check_param_type():
    global param_count, hasParam, acounter
    data.description=request.form['desc']
    data.questionGroup=request.form['group']
    if type == 'MCQ' or type == 'MCMR':
        counter=request.form['counter']
        if (counter>0):
            hasParam=1
        param_count=int(counter)
        print 'HasParam:', hasParam
        print data.description
        print param_count 
        return render_template('check_param_type.html', param_count=range(param_count))
    elif type=='FIB':
        qcounter=int(request.form.get('q_counter'))
        acounter=int(request.form.get('a_counter'))
        if (qcounter>0):
            hasParam=1
        param_count=qcounter
        print 'HasParam:', hasParam
        print data.description
        print param_count 
        return render_template('FIB_check_param_type.html', param_count=range(param_count))
  
    
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    
params=[]
varVal=1

@app.route('/insert_params', methods=['POST'])
def insert_params():
    global params
    global param_count, acounter
    #print(range(int(param_count)))
    print param_count
    print acounter
    #print type(param_count)
    for i in range(param_count):
        params.append(request.form[str(i)])
        #INSERT PARAMS INTO DATABASE
        params[i]=int(params[i])
    print params
    if type == 'MCQ' or type == 'MCMR': 
        return render_template('insert_params.html', params=params)
    else:
        return render_template('FIB_insert_params.html', params=params, acounter=acounter)

textVar=[]
imageVar=[]
filename=[]
ansVar = []
# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    global textVar, imageVar, filename, ansVar
    global varVal
    j=0
    # Get the name of the uploaded file
    for i in range(param_count):
        if params[i]==0:
            textVar=request.form.getlist('text_file')
                
        else:
            imageVar=request.files.getlist('image_file')
            print imageVar
            filename.append(secure_filename(imageVar[j].filename))
            # Move the file form the temporal folder to
            # the upload folder we setup
            imageVar[j].save(os.path.join(app.config['UPLOAD_FOLDER'], filename[j]))
            j=j+1
            print imageVar
    varVal = int(request.form.get('param_var'))
    ansVar = request.form.getlist('text_ans')
    print varVal
    if type=='FIB':
        return redirect(url_for('insert_choices'))
    else:
        return render_template('check_variations.html', varVal=varVal, type=type)
                
global question
question=[]
answer=[]

data.ques=list(list())
data.ans=list(list())

def insert_MCQ_QnA(varVal,answer):
        ans=list(list())
        print 'ANS varVal, answer',ans, varVal, answer
        for var in range(varVal):
            choiceVal = request.form.getlist('value'+str(var))
            print 'choiceVal:', choiceVal
            right = request.form.getlist('right'+str(var))
            print 'right:', right
            for choiceNo in range(len(right)): 
                answer.append(str(var))
                print answer
                answer.append(str(choiceNo))
                answer.append(str(choiceVal[choiceNo]))
                if str(right[choiceNo])=='1':
                    answer.append('correct')
                    print answer
                else:
                    answer.append('wrong')
                    print answer
                ans.append(answer)
                answer=[]
        return ans
            
        
                
@app.route('/question_congrats', methods=['POST','GET'])
def insert_choices():
    global params, question, db, data, varVal, answer
    print varVal, params, hasParam, answer
    print 'WALAO starts!'
    i,j = 0,0
    if type=='MCQ' or type=='MCMR:'
    for var in range(varVal):
        for param in params:
            question.append(str(hasParam))
            print question
            question.append(str(var))
            print question
            question.append(str(param))
            if param==0:
                question.append('text')
                print question
                question.append(str(textVar[i]))
                print question
                i=i+1
            else:
                question.append('image')
                print question
                question.append(str(imageVar[j].filename))
                print question
                j=j+1
            data.ques.append(question)
            question=[]
    data.ans = insert_MCQ_QnA(varVal, answer)
    print data.ques, data.ans   
    db.session.add((QnA(questionNo=890,questionGroup=data.questionGroup, questionType=type)))
    db.session.add((MCQMCMR(questionNo=890,description=data.description, ques=data.ques, ans=data.ans)))
    db.session.commit()
    
    
    return render_template('congrats.html')



# @app.route('/question_congrats', methods=['POST'])
# def question_congrats():
#     
#     return render_template('question_congrats.html')




if __name__=='__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.run(debug=True)
