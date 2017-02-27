from flask import Flask, render_template, request
from QnA import dbsession, qQues

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Read the HTTP POST request parameter from request.form
    user = request.form['mailid']
    password = request.form['pass']
    option = request.form['option']
    # Validate and send response
    if (user and password and option):
        #flag=insert_login(user,password,option)
        flag = 1
        if flag==0:
            return render_template('index.html')
        else:
            import QnA
            return render_template('question.html',qQues=qQues)
    else:
        return 'Please go back and enter the details...'
        
if __name__ == '__main__':
    app.run(debug=True)
