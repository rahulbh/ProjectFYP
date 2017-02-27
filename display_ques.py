import QnA
picker=QnA.def_picker()
QnA.pick_ques(QnA.qQues, picker)

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('disp.html',qQues=QnA.qQues)

if __name__ == '__main__':
    app.run(debug=True)