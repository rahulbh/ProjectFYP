from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref

db=SQLAlchemy()

class QnA(db.Model):
    __tablename__ = 'QnA'
    
    questionno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    questiongroup = db.Column(db.String(64))
    questiontype = db.Column(db.Enum('MCQ', 'MCMR', 'SA', 'FIB', name='type_enum'), nullable = False, default= 'MCQ')
    #imgData = db.Column(db.String(256))
    #description = db.Column(db.TEXT, nullable = False)
    remarks = db.Column (db.String(2048))
    maxmarks = db.Column(db.Integer, nullable = False)
    coursecode  = db.Column (db.String(8), db.ForeignKey('Courses.coursecode'))
    
    MCQQnA = db.relationship("MCQMCMR", uselist=False, backref=db.backref("QnA", uselist=False))
    SA = db.relationship("SA", uselist=False, backref=db.backref("QnA", uselist=False))
    FIB = db.relationship("FIB", uselist=False, backref=db.backref("QnA", uselist=False))
    Courses = db.relationship('Courses', backref=db.backref('QnA', lazy='dynamic'))
    #specassesments = db.relationship('SpecificAssessment', backref=db.backref('QnA', lazy='dynamic'))
    
    
    #ques = db.Column (postgresql.ARRAY(db.String(64), dimensions = 2))
    #ans = db.Column (postgresql.ARRAY(db.String(64), dimensions=2),default=0)
    
class MCQMCMR(db.Model):
    __tablename__ = 'MCQMCMR'
    questionno = db.Column(db.Integer,  db.ForeignKey('QnA.questionno'),primary_key=True)
    ques = db.Column (postgresql.ARRAY(db.String(64), dimensions = 2))
    description = db.Column(db.TEXT, nullable = False)
    ans = db.Column (postgresql.ARRAY(db.String(64), dimensions=2),default=0)
    partialmarks = db.Column(db.Integer, default=0)
    
class SA(db.Model):
    __tablename__ = 'SA'
    questionno = db.Column(db.Integer, db.ForeignKey('QnA.questionno'), primary_key=True)
    ques = db.Column (postgresql.ARRAY(db.String(64), dimensions = 2))
    description = db.Column(db.TEXT, nullable = False)
    ans = db.Column (postgresql.ARRAY(db.String(64), dimensions=2),default=0)
    datatype = db.Column(db.Enum('String', 'Float', 'Integer', name='data_enum'), nullable = False, default= 'MCQ')
    tolerance = db.Column(db.Float)
    
class FIB(db.Model):
    __tablename__ = 'FIB'
    questionno = db.Column(db.Integer, db.ForeignKey('QnA.questionno'), primary_key=True)
    ques = db.Column (postgresql.ARRAY(db.String(64), dimensions = 2))
    description = db.Column(db.TEXT, nullable = False)
    ans = db.Column (postgresql.ARRAY(db.String(64), dimensions=2),default=0)
    datatype = db.Column(db.Enum('String', 'Float', 'Integer', name='data_enum'), nullable = False, default= 'MCQ')
    tolerance = db.Column(db.Float)
    
class Courses(db.Model):
    __tablename__ = 'Courses'
    coursecode = db.Column(db.String(8),  primary_key=True)
    coursetitle  = db.Column (db.String(64))
    
class CourseGroupUsers(db.Model):
    __tablename__ = 'CourseGroupUsers'
    loginid = db.Column(db.String(15), db.ForeignKey('Users.userid'),  primary_key=True)
    coursecode  = db.Column (db.String(8), db.ForeignKey('Courses.coursecode'), primary_key=True)
    
class Users(db.Model):
    __tablename__ = 'Users'
    userid = db.Column(db.String(15),  primary_key=True)
    password = db.Column (db.String(32))
    role = db.Column(db.Enum('INSTRUCT', 'STUD', 'ADMIN',  name='role_enum'), nullable = False, default= 'STUD')
    superuser = db.Column (db.Boolean, default = False)
    
class Submission(db.Model):
    __tablename__ = 'Submission'
    coursecode  = db.Column (db.String(8), db.ForeignKey('Courses.coursecode'))
    assessmentno = db.Column (db.Integer, db.ForeignKey('Assessments.assessmentno'))
    loginid = db.Column(db.String(15), db.ForeignKey('Users.userid'))
    uploadtime = db.Column (db.DateTime)
    totalmark = db.Column (db.Float, nullable = False)
    finalmark = db.Column (db.Float, nullable = False)
    submissionno = db.Column (db.Integer, primary_key=True)
    filename = db.Column (db.String(128))
    
class Assessments(db.Model):
    __tablename__ = 'Assessments'
    coursecode  = db.Column (db.String(8), db.ForeignKey('Courses.coursecode'))
    assessmentno = db.Column (db.Integer, primary_key = True, autoincrement=True )
    title = db.Column(db.String(128))
    duration = db.Column (db.Integer, nullable = False)
    enabled = db.Column (db.Boolean, default = True)
    message = db.Column (db.String(8192))
    location = db.Column (db.Enum('BEG', 'END', name='loc_enum'))
    israndomq = db.Column(db.Boolean)
    israndoma = db.Column(db.Boolean)
    
    assesments = db.relationship('SpecificAssessment', backref=db.backref('Assessments'))
    submission = db.relationship('Submission', backref=db.backref('Assessments'))
    
class SpecificAssessment(db.Model):
    __tablename__ = 'SpecificAssessment'
    questiontype = db.Column(db.Enum('MCQ', 'MCMR', 'SA', 'FIB', name='type_enum'), primary_key = True)
    assessmentno = db.Column (db.Integer, db.ForeignKey('Assessments.assessmentno'), primary_key = True)
    questiongroup = db.Column(db.String(64), primary_key = True)
    number = db.Column (postgresql.ARRAY(db.String(10), dimensions=1))
    coursecode  = db.Column (db.String(8), db.ForeignKey('Courses.coursecode'), primary_key=True)
    


    
    
def load_db(db):
    """Create database tables and insert records"""
    # Drop and re-create all the tables.
    db.drop_all()
    db.create_all()
    db.session.commit()
    db.session.add(Courses(coursecode='EE0040', coursetitle='Engineers And Society'))
    db.session.commit()
    db.session.add(Users(userid='rahul009', password='password', role='STUD', superuser=True))
    db.session.commit()
    db.session.add(CourseGroupUsers(loginid='rahul009', coursecode='EE0040'))
    db.session.commit()


    testcases=[{"questionno":801, "questiongroup":"General Science","description":"This question does not relate to the image! Suppose that you plucked %%P%% apples,and Steve took away three. How many apples do you have?"\
            ,"ques":[['1','0','0','text','five'],['1','1','0','text','six']],"ans":[['0','0','10','0'],['0','1','11','0'],['0','2','2','1'],['0','3','13','0'],['0','4','14','0'],['1','0','21','0'],\
                                                                      ['1','1','22','0'],['1','2','23','0'],['1','3','24','0'],['1','4','All of the Above','0'],['1','5','None of the Above','1']],"remarks":"Hello 801"},\
                {"questionno":802,"questiongroup":"General Science","description":"What's the value of Resistance of LDR? %%P%% "\
            ,"ques":[['1','0','0','image','LDR-circuit-improved.png']],"ans":[['0','0','10 ohm','0'],['0','1','15 ohm','1'],['0','2','15 ohm','0'],['0','3','20 ohm','0']],"remarks":"Hello 802"},\
           \
           {"questionno":803,"questiongroup":"General Science","description":"Which scientist created e=mc<sup>2</sup>??"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','Issac Newtown','0'],['0','1','Charles Darwin','0'],['0','2','Albert Einstein','1'],['0','3','Michael Faraday','0']],"remarks":"Hello 803"},\
           \
           {"questionno":804,"questiongroup":"Air and Atmosphere","description":"Nitrogen is obtained from fractional distillation of liquefied air at about"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','196 C','0'],['0','1','186 C','1'],['0','2','176 C','0'],['0','3','166 C','0']],"remarks":"Hello 804"},\
           \
           {"questionno":805,"questiongroup":"Air and Atmosphere","description":"A greenhouse gas that absorbs energy and maintains earth's temperature is"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','carbon dioxide','1'],['0','1','oxygen','0'],['0','2','nitrogen','0'],['0','3','argon','0']],"remarks":"Hello 805"},\
           \
           {"questionno":806,"questiongroup":"Air and Atmosphere","description":"Main constituent in air is"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','nitrogen','1'],['0','1','oxygen','0'],['0','2','argon','0'],['0','3','water vapor','0']],"remarks":"Hello 806"},\
           \
           {"questionno":807,"questiongroup":"Air and Atmosphere","description":"On cooling, a liquid will be changed into"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','dense','0'],['0','1','solid','1'],['0','2','semi-solid','0'],['0','3','liquid','0']],"remarks":"Hello 807"},\
           \
           {"questionno":808,"questiongroup":"Air and Atmosphere","description":"Combustion cannot take place without %%P%%"\
            ,"ques":[['1','0','0','image', 'Combustion_reaction_of_methane.jpg']],"ans":[['0','0','water','0'],['0','1','carbon','0'],['0','2','air','1'],['0','3','zinc','0']],"remarks":"Hello 808"},\
           \
           {"questionno":809,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"Remaining solid on filter paper is known as"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','solution','0'],['0','1','stone','0'],['0','2','particles','0'],['0','3','residue','1']],"remarks":"Hello 809"},\
           \
           {"questionno":810,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"Letter used to identify an element in periodic table is known as"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','formula','0'],['0','1','idea','0'],['0','2','symbol','1'],['0','3','hint','0']],"remarks":"Hello 810"},\
           \
           {"questionno":811,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"A component of plant cell that is absent in animal cell is known as"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','cell membrane','0'],['0','1','cytoplasm','0'],['0','2','nucleus','0'],['0','3','Cellulose','1']],"remarks":"Hello 811"},\
           \
           {"questionno":812,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"For lowering body tube until objective is 0.25 inches of object, we use"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','illumination','0'],['0','1','Stage','0'],['0','2','diaphragm','0'],['0','3','coarse focus','1']],"remarks":"Hello 812"},\
           \
           {"questionno":813,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"Smallest cells present in human body are"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','red blood','0'],['0','1','brain cells','1'],['0','2','egg-cell','0'],['0','3','nerve','0']],"remarks":"Hello 813"}];
            
    testcasesmcmr=[{"questionno":814, "questiongroup":"General Science","description":"This question does not relate to the image! Suppose that you plucked %%P%% apples,and Steve took away three. How many apples do you have?"\
            ,"ques":[['1','0','0','text','five'],['1','1','0','text','six']],"ans":[['0','0','10','1'],['0','1','11','0'],['0','2','2','1'],['0','3','13','0'],['0','4','14','0'],['1','0','21','0'],\
                                                                      ['1','1','22','0'],['1','2','23','0'],['1','3','24','0'],['1','4','All of the Above','0'],['1','5','None of the Above','1']],"remarks":"Hello 801"},\
                {"questionno":815,"questiongroup":"General Science","description":"What's the value of Resistance of LDR? %%P%% "\
            ,"ques":[['1','0','0','image','LDR-circuit-improved.png']],"ans":[['0','0','10 ohm','1'],['0','1','15 ohm','1'],['0','2','15 ohm','0'],['0','3','20 ohm','0']],"remarks":"Hello 802"},\
           \
           {"questionno":816,"questiongroup":"General Science","description":"Which scientist created e=mc<sup>2</sup>??"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','Issac Newtown','0'],['0','1','Charles Darwin','1'],['0','2','Albert Einstein','1'],['0','3','Michael Faraday','0']],"remarks":"Hello 803"},\
           \
           {"questionno":817,"questiongroup":"Air and Atmosphere","description":"Nitrogen is obtained from fractional distillation of liquefied air at about"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','196 C','0'],['0','1','186 C','1'],['0','2','176 C','1'],['0','3','166 C','0']],"remarks":"Hello 804"},\
           \
           {"questionno":818,"questiongroup":"Air and Atmosphere","description":"A greenhouse gas that absorbs energy and maintains earth's temperature is"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','carbon dioxide','1'],['0','1','oxygen','0'],['0','2','nitrogen','1'],['0','3','argon','0']],"remarks":"Hello 805"},\
           \
           {"questionno":819,"questiongroup":"Air and Atmosphere","description":"Main constituent in air is"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','nitrogen','1'],['0','1','oxygen','0'],['0','2','argon','1'],['0','3','water vapor','0']],"remarks":"Hello 806"},\
           \
           {"questionno":820,"questiongroup":"Air and Atmosphere","description":"On cooling, a liquid will be changed into"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','dense','0'],['0','1','solid','1'],['0','2','semi-solid','1'],['0','3','liquid','0']],"remarks":"Hello 807"},\
           \
           {"questionno":821,"questiongroup":"Air and Atmosphere","description":"Combustion cannot take place without %%P%%"\
            ,"ques":[['1','0','0','image', 'Combustion_reaction_of_methane.jpg']],"ans":[['0','0','water','1'],['0','1','carbon','0'],['0','2','air','1'],['0','3','zinc','0']],"remarks":"Hello 808"},\
           \
           {"questionno":822,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"Remaining solid on filter paper is known as"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','solution','0'],['0','1','stone','1'],['0','2','particles','0'],['0','3','residue','1']],"remarks":"Hello 809"},\
           \
           {"questionno":823,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"Letter used to identify an element in periodic table is known as"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','formula','0'],['0','1','idea','1'],['0','2','symbol','1'],['0','3','hint','0']],"remarks":"Hello 810"},\
           \
           {"questionno":824,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"A component of plant cell that is absent in animal cell is known as"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','cell membrane','0'],['0','1','cytoplasm','1'],['0','2','nucleus','0'],['0','3','Cellulose','1']],"remarks":"Hello 811"},\
           \
           {"questionno":825,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"For lowering body tube until objective is 0.25 inches of object, we use"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','illumination','0'],['0','1','Stage','1'],['0','2','diaphragm','0'],['0','3','coarse focus','1']],"remarks":"Hello 812"},\
           \
           {"questionno":826,"questiongroup":"Atoms Molecules Mixtures and Compounds","description":"Smallest cells present in human body are"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','red blood','1'],['0','1','brain cells','1'],['0','2','egg-cell','0'],['0','3','nerve','0']],"remarks":"Hello 813"}];
    
    
    for t in testcases:
        db.session.add(QnA(questionno=t['questionno'], questiongroup=t['questiongroup'], questiontype = 'MCQ', remarks=t['remarks'], maxmarks=4, coursecode='EE0040'))
        db.session.add(MCQMCMR(questionno=t['questionno'], description=t['description'], ques=t['ques'], ans=t['ans']))
        db.session.commit()
        
    for t in testcasesmcmr:
        db.session.add(QnA(questionno=t['questionno'], questiongroup=t['questiongroup'], questiontype = 'MCMR', remarks=t['remarks'], maxmarks=4, coursecode='EE0040'))
        db.session.add(MCQMCMR(questionno=t['questionno'], description=t['description'], ques=t['ques'], ans=t['ans']))
        db.session.commit()

