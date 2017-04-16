from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from wtforms import Form, RadioField
import os
from wtforms import TextField, validators, PasswordField, TextAreaField, HiddenField, SubmitField
from db_init_final import QnA, db, load_db, MCQMCMR, FIB, Assessments, SA, SpecificAssessment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func, Select
import random
import subprocess
import os
import stat


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
db.session.expire_on_commit=False 

@app.route('/')
def insert_title():
    #title=request.form['title']
    title="SAMPLE QUIZ"
    if title:
        return render_template("general_options.html", title=title)
    
    else:
        return render_template("home_instructor.html")
    

quesTop = 0
seq = 0

@app.route('/open_shell')
def open_shell():
    st = os.stat('test.sh')
    os.chmod('test.sh', st.st_mode | stat.S_IEXEC)
    subprocess.call(['./test.sh'])
    title = 'SAMPLE_QUIZ'
    return render_template("general_options1.html", title=title)
    
#This function is to generate a table of available number of question from each group, 
#so that the instructor can select the number of questions to pick from for each topic



@app.route('/generate_assessment')
def generate_assessment():
    global db
    mcq = list()
    detailmcq = list()
    mcmr = list()
    detailmcmr = list()
    fib = list()
    detailfib = list()
    sa = list()
    detailsa = list()
    
    ques_brief = list()
    ques_det = list()
    for instance in db.session.query(Assessments).filter_by(enabled=True).all():
        active_ass = instance
        
    print active_ass.assessmentno
    
    #spec_ass = db.session.query(SpecificAssessment).filter_by(assessmentno=active_ass.assessmentno)
    #spec_ass_MCQ = db.session.query(SpecificAssessment).filter_by(questiontype='MCQ')
    #spec_ass_MCMR = db.session.query(SpecificAssessment).filter_by(questiontype='MCMR')
    #spec_ass_FIB = db.session.query(SpecificAssessment).filter_by(questiontype='FIB')
    #spec_ass_SA = db.session.query(SpecificAssessment).filter_by(questiontype='SA')
    for instance in db.session.query(SpecificAssessment).filter_by(assessmentno=active_ass.assessmentno):
        questions = instance.number
        print 'NUMBER OF QUES', instance.number
        for j in range(len(questions)):
            for ins in db.session.query(QnA).filter_by(questionno=questions[j]).all():
                if ins.questiontype == 'MCQ':
                    mcq.append(ins)
                    print mcq[0].questionno
                    for sample in db.session.query(MCQMCMR).filter_by(questionno=ins.questionno).all():
                        detailmcq.append(sample)
                        print 'WALAOOOOOOOOOOOOOOOOOOOOO', sample.questionno
                elif ins.questiontype == 'MCMR':
                    mcmr.append(ins)
                    for sample in db.session.query(MCQMCMR).filter_by(questionno=ins.questionno).all():
                        detailmcmr.append(sample)
                elif ins.questiontype == 'FIB':
                    fib.append(ins)
                    for sample in db.session.query(FIB).filter_by(questionno=ins.questionno).all():
                        detailfib.append(sample)
                elif ins.questiontype == 'SA':
                    sa.append(ins)
                    for sample in db.session.query(SA).filter_by(questionno=ins.questionno).all():
                        detailsa.append(sample)
                print ins.questiontype
                
    return render_template('sample_assessment.html', mcq = mcq, mcmr = mcmr, fib = fib, sa = sa, detailmcq = detailmcq, detailmcmr = detailmcmr, detailsa = detailsa, detailfib = detailfib )
        
         
title  = ''
random_ques=False
random_ans=False
max_time=0
coursecode='EE0040'
location='BEG'
#    return render_template('sample_assessment.html')

@app.route('/insert_GO', methods=['POST'])
def insert_GO():
    #print request.form.get('random_questions')
    #print request.form.get('random_answers')
    global title, random_ans, random_ques, coursecode
    title = request.form.get('title')
    if request.form.get('random_questions')=='yes_display':
        random_ques=True
        #print 'Random Question'
    if request.form.get('random_answers')=='yes_display':
        random_ans=True
        #print 'Random Answer'    
    max_time=request.form.get('time')
    print 'Time',max_time
    #PUT VALUES IN DATABSE
    
    return render_template("custom_messages.html")


ass =0
assno=0
cocode=0

@app.route('/congrats', methods=['POST'])
def congrats():
    global location, max_time, message, coursecode, title, random_ques, random_ans, ass
    global assno, cocode
    #PUT VALUES IN DATABASE
    message=request.form.getlist('message')
    if(len(message)>0):
        if(message[0].len()>1):
            message=message[0]
            location='BEG'
        elif(message[1].len()>1):
            message=message[1]
            location='END'
    ass = Assessments(coursecode=coursecode, message=message, location=location, title=title, duration=max_time, enabled=True, israndomq=random_ques, israndoma=random_ans)
    db.session.add(ass)
    db.session.flush()
    assno =ass.assessmentno
    cocode = ass.coursecode
    db.session.commit()
    return render_template("congrats.html")

@app.route('/pick_questions')
def pick_questions():
    allQues=dict()
    allGroups=db.session.query(QnA.questiongroup).distinct().all()
    print allGroups
    for group in allGroups:
        allQues[group]=db.session.query(QnA).filter_by(questiongroup=group).all()
        print allQues[group]
    return render_template('pick_questions.html', allQues=allQues, allGroups=allGroups)

@app.route('/add_questions_assessment', methods=['POST'])
def add_questions_assessment():
    global assno, cocode
    mydict=dict()
    scope = list
    j=0
    numbers=db.session.query(QnA.questionno).all()
    scope=list(list())
    for i in range(len(numbers)):
        print 'indi number', isinstance(numbers[i], tuple)
        #print numbers[i]
        numbers[i]=str(numbers[i]).translate(None, ",()")
        numbers[i]=''.join(map(str, numbers[i]))
        #print request.form.get(numbers[i])
        if request.form.get(str(numbers[i]))=='checked':
            print 'HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
            qgroup=str(db.session.query(QnA.questiongroup).filter_by(questionno=numbers[i]).scalar())
            qtype = db.session.query(QnA.questiontype).filter_by(questionno=numbers[i]).scalar()
            print qgroup, qtype
            list_scope=(qgroup, qtype)
            scope.append(list_scope)
            if mydict.has_key(scope[j]):
                mydict[list_scope].append(numbers[i])
            else:
                mydict[list_scope] = [numbers[i]]
            print mydict[scope[j]]
            j=j+1
            
    for i in range(len(scope)):
        print 'TUPLE', scope[i]
        qgroup = scope[i][0]
        qtype = scope[i][1]
        len_scope=len(scope[i])
        print assno
        print cocode
        print qtype, qgroup, mydict[scope[i]]
        #map(db.session.refresh, iter(db.session))  # call refresh() on every instance
        db.session.add(SpecificAssessment(assessmentno=assno, coursecode=cocode, questiontype=qtype, questiongroup=qgroup, number=mydict[scope[i]]))
        db.session.commit()
    return render_template('general_options.html')




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
    print type
    type=request.form['type']
    form=QuestionDesc()
    if(type=='MCQ' or type=='MCMR'):
        return render_template('insert_question_text.html', form=form)
    elif(type=='FIB'):
        return render_template('FIB_insert_question_text.html', form=form)
    else:
        return render_template('insert_question_text.html', form=form)
        
    
param_count=0
hasParam=0
acounter=0


@app.route('/check_param_type', methods=['POST'])
def check_param_type():
    global param_count, hasParam, acounter
    data.description=request.form['desc']
    data.questionGroup=request.form['group']
    data.maxmarks=int(request.form.get('max_marks'))
    if type == 'MCQ' or type == 'MCMR' or type == 'SA':
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
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    
params=[]
varVal=1
type=''

@app.route('/insert_params', methods=['POST'])
def insert_params():
    global params
    global param_count, acounter, type
    #print(range(int(param_count)))
    print param_count #Number of Question Parameters
    print acounter #Number of Answer Parameters
    #print type(param_count)
    for i in range(param_count):
        params.append(request.form[str(i)]) 
        params[i]=int(params[i])  
    print params
    if type == 'MCQ' or type == 'MCMR' : 
        return render_template('insert_params.html', params=params)
    elif type == 'FIB':
        return render_template('FIB_insert_params.html', params=params, acounter=acounter)
    else:
        return render_template('SA_insert_params.html', params=params)
    
textVar=[]
imageVar=[]
filename=[]
ansVarFIBSA = []
# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    global textVar, imageVar, filename, ansVarFIBSA, type
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
    varVal = int(request.form.get('param_var')) #Number of Variations
    ansVarFIBSA = request.form.getlist('text_ans')
    data.tolerance=request.form.get('tolerance')
    data.datatype=request.form.get('ans_type')
    print varVal 
    if type=='FIB' or type == 'SA':
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
    
def insert_FIB_QnA(varVal,answer):
        ans=list(list())
        i=0
        global ansVarFIBSA
        print 'ANS varVal, answer',ans, varVal, ansVarFIBSA
        for var in range(varVal):
            print 'ANSWERS:', ansVarFIBSA
            for ansNo in range(len(ansVarFIBSA)/varVal): 
                answer.append(str(var))
                print answer
                answer.append(str(ansNo))
                answer.append(str(ansVarFIBSA[i]))
                i=i+1
                ans.append(answer)
                answer=[]
        return ans
            
        
partial_marks=0                
@app.route('/question_congrats', methods=['POST','GET'])
def insert_choices():
    global params, question, db, data, varVal, answer, partial_marks
    print varVal, params, hasParam, answer
    print 'WALAO starts!'
    i,j = 0,0
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
    print type
    if type=='MCQ' or type=='MCMR':
        data.ans = insert_MCQ_QnA(varVal, answer)
        if type=='MCMR':
            data.partialmarks=request.form.get('partial_marks')
        print data.ques, data.ans   
        db.session.add((QnA(questionno=890,questiongroup=data.questionGroup, questiontype=type, coursecode='EE0040', maxmarks=data.maxmarks)))

        db.session.add((MCQMCMR(questionno=890,description=data.description, ques=data.ques, ans=data.ans, partialmarks=data.partialmarks)))
        db.session.commit()
    elif type=='FIB':
        data.ans = insert_FIB_QnA(varVal, answer)
        print data.ans
        db.session.add((QnA(questionno=890,questiongroup=data.questionGroup, questiontype=type, coursecode='EE0040', maxmarks=data.maxmarks)))
        db.session.add((FIB(questionno=890,description=data.description, ques=data.ques, ans=data.ans, tolerance=data.tolerance, datatype=data.datatype)))
        db.session.commit()
    elif type == 'SA':
        data.ans = insert_FIB_QnA(varVal, answer)
        print data.ans
        db.session.add((QnA(questionno=890,questiongroup=data.questionGroup, questiontype=type, coursecode='EE0040', maxmarks=data.maxmarks)))
        db.session.add((SA(questionno=890,description=data.description, ques=data.ques, ans=data.ans, tolerance=data.tolerance, datatype=data.datatype)))
        db.session.commit()
    
        
    data,params,question,varVal=0,0,0,0
    return render_template('question_congrats.html')



# @app.route('/question_congrats', methods=['POST'])
# def question_congrats():
#     
#     return render_template('question_congrats.html')




if __name__=='__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.run(debug=True)
