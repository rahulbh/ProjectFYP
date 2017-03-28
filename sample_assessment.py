from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from wtforms import Form, RadioField
import os
from wtforms import TextField, validators, PasswordField, TextAreaField, HiddenField, SubmitField
from db_init_final import QnA, db, load_db, MCQMCMR, FIB
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.functions import func
#from insert_QnA_data import insert_MCQ_QnA

# Flask: Initialize
app = Flask(__name__)
 
# Flask-SQLAlchemy: Initialize
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testuser:test123@localhost:5432/testdb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testuser:xxxx@localhost:5432/testdb'
db.init_app(app)   # Bind SQLAlchemy to this Flask app

@app.route('/generate_question')
def generate_question():
    quesTop = QnA.query(QnA.questionGroup, func(sum(QnA.questionGroup))).group_by(QnA.questionGroup)
    print quesTop
    return render_template('question_picker.html', quesTop)



if __name__=='__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.run(debug=True)    