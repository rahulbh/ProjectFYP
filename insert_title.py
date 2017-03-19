from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from wtforms import Form, RadioField
import os
from wtforms import TextField, validators, PasswordField, TextAreaField, HiddenField, SubmitField
from db_init import db, load_db, QnA

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
        submit = SubmitField('submit')
        
        
@app.route('/insert_question_text', methods=['POST'])
def insert_question_text():
    #type=request.form['type']
    form=QuestionDesc()
    #if(type=='MCQ'):
    return render_template('insert_question_text.html', form=form)
    
param_count=0
@app.route('/check_param_type', methods=['POST'])
def check_param_type():
    global param_count
    
    param_count=request.form['counter']
    print param_count   
    return render_template('check_param_type.html', param_count=range(int(param_count)))
    
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    
params=[]

@app.route('/insert_params', methods=['POST'])
def insert_params():
    global params
    global param_count
    #print(range(int(param_count)))
    print param_count
    param_count=int(param_count)
    print type(param_count)
    for i in range(param_count):
        params.append(request.form[str(i)])
        #INSERT PARAMS INTO DATABASE
        params[i]=int(params[i])
    return render_template('insert_params.html', params=params)


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    textVar=[]
    imageVar=[]
    # Get the name of the uploaded file
    for i in range(param_count):
        if params[i]==0:
            textVar.append(request.form['text_file'+str(i)])
            print textVar[i]
        else:
            imageVar=request.files['image_file'+str(i)]
            filename = secure_filename(imageVar.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            imageVar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('check_varations.html')
      
                
                
@app.route('/insert_choices', methods=['POST'])
def insert_choices():
    return render_template('insert_choices.html')

if __name__=='__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.run(debug=True)
