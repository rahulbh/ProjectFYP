from flask import Flask, render_template, request
from wtforms import Form, RadioField
from wtforms import TextField, validators, PasswordField, TextAreaField, HiddenField, SubmitField

app = Flask(__name__)



@app.route('/',methods=['POST'])
def main():
    
    
    if title:
        return render_template("general_options.html", title=title)
    
    else:
        return render_template("home_instructor.html")



app.run(debug=True)