from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql



db=SQLAlchemy()

class QnA(db.Model):
    __tablename__ = 'QnA'
    
    questionNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    questionGroup = db.Column(db.String(64))
    questionType = db.Column(db.Enum('MCQ', 'MCMR', 'SA', 'FIB', name='type_enum'), nullable = False, default= 'MCQ')
    #imgData = db.Column(db.String(256))
    #description = db.Column(db.TEXT, nullable = False)
    remarks = db.Column (db.String(2048))
    MCQQnA = db.relationship("MCQMCMR", uselist=False, backref=db.backref("QnA", uselist=False))
    SA = db.relationship("SA", uselist=False, backref=db.backref("QnA", uselist=False))
    FIB = db.relationship("FIB", uselist=False, backref=db.backref("QnA", uselist=False))
    
    
    #ques = db.Column (postgresql.ARRAY(db.String(64), dimensions = 2))
    #ans = db.Column (postgresql.ARRAY(db.String(64), dimensions=2),default=0)
    
class MCQMCMR(db.Model):
    __tablename__ = 'MCQMCMR'
    questionNo = db.Column(db.Integer,  db.ForeignKey('QnA.questionNo'),primary_key=True)
    ques = db.Column (postgresql.ARRAY(db.String(64), dimensions = 2))
    description = db.Column(db.TEXT, nullable = False)
    ans = db.Column (postgresql.ARRAY(db.String(64), dimensions=2),default=0)
    
class SA(db.Model):
    __tablename__ = 'SA'
    questionNo = db.Column(db.Integer, db.ForeignKey('QnA.questionNo'), primary_key=True)
    ques = db.Column (postgresql.ARRAY(db.String(64), dimensions = 2))
    description = db.Column(db.TEXT, nullable = False)
    ans = db.Column (postgresql.ARRAY(db.String(64), dimensions=2),default=0)
    
class FIB(db.Model):
    __tablename__ = 'FIB'
    questionNo = db.Column(db.Integer, db.ForeignKey('QnA.questionNo'), primary_key=True)
    ques = db.Column (postgresql.ARRAY(db.String(64), dimensions = 2))
    description = db.Column(db.TEXT, nullable = False)
    ans = db.Column (postgresql.ARRAY(db.String(64), dimensions=2),default=0)
    

    
    
def load_db(db):
    """Create database tables and insert records"""
    # Drop and re-create all the tables.
    db.drop_all()
    db.create_all()
    


    
    testcases=[{"questionNo":801, "questionGroup":"General Science","description":"This question does not relate to the image! Suppose that you plucked %%P1%% apples,and Steve took away three. How many apples do you have?"\
            ,"ques":[['1','0','0','text','five'],['1','1','0','text','six']],"ans":[['0','0','10','0'],['0','1','11','0'],['0','2','2','1'],['0','3','13','0'],['0','4','14','0'],['1','0','21','0'],\
                                                                      ['1','1','22','0'],['1','2','23','0'],['1','3','24','0'],['1','4','All of the Above','0'],['1','5','None of the Above','1']],"remarks":"Hello 801"}]
            
    for t in testcases:
        db.session.add(QnA(questionNo=t['questionNo'], questionGroup=t['questionGroup'], questionType = 'MCQ', remarks=t['remarks']))
        db.session.add(MCQMCMR(questionNo=t['questionNo'], description=t['description'], ques=t['ques'], ans=t['ans']))
        db.session.commit()

