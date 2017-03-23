from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

db=SQLAlchemy()

class QnA(db.Model):
    __tablename__ = 'QnA'
    
    questionNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    questionGroup = db.Column(db.String(64))
    #imgData = db.Column(db.String(256))
    description = db.Column(db.TEXT)
    remarks = db.Column (db.String(2048))
    ques = db.Column (postgresql.ARRAY(db.String(64), dimensions = 2))
    ans = db.Column (postgresql.ARRAY(db.String(64), dimensions=2),default=0)
    
def load_db(db):
    """Create database tables and insert records"""
    # Drop and re-create all the tables.
    db.drop_all()
    db.create_all()
    
    testcases=[{"questionNo":801, "questionGroup":"General Science","description":"This question does not relate to the image! Suppose that you plucked %%P1%% apples,and Steve took away three. How many apples do you have?"\
            ,"ques":[['1','0','0','text','five'],['1','1','0','text','six']],"ans":[['0','0','10','0'],['0','1','11','0'],['0','2','2','1'],['0','3','13','0'],['0','4','14','0'],['1','0','21','0'],\
                                                                      ['1','1','22','0'],['1','2','23','0'],['1','3','24','0'],['1','4','All of the Above','0'],['1','5','None of the Above','1']],"remarks":"Hello 801"},\
           {"questionNo":802,"questionGroup":"General Science","description":"Which scientist developed the theory of universal gravitation?"\
            ,"ques":[['0','0','0','0','0'],['0','0','0','0','0']],"ans":[['0','0','Issac Newtown','0'],['0','1','Charles Darwin','1'],['0','2','Albert Einstein','0'],['0','3','Michael Faraday','0']],"remarks":"Hello 802"},\
           \
           {"questionNo":803,"questionGroup":"General Science","description":"Which scientist created e=mc<sup>2</sup>??"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','Issac Newtown','0'],['0','1','Charles Darwin','0'],['0','2','Albert Einstein','1'],['0','3','Michael Faraday','0']],"remarks":"Hello 803"},\
           \
           {"questionNo":804,"questionGroup":"Air and Atmosphere","description":"Nitrogen is obtained from fractional distillation of liquefied air at about"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','196 C','0'],['0','1','186 C','1'],['0','2','176 C','0'],['0','3','166 C','0']],"remarks":"Hello 804"},\
           \
           {"questionNo":805,"questionGroup":"Air and Atmosphere","description":"A greenhouse gas that absorbs energy and maintains earth's temperature is"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','carbon dioxide','1'],['0','1','oxygen','0'],['0','2','nitrogen','0'],['0','3','argon','0']],"remarks":"Hello 805"},\
           \
           {"questionNo":806,"questionGroup":"Air and Atmosphere","description":"Main constituent in air is"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','nitrogen','1'],['0','1','oxygen','0'],['0','2','argon','0'],['0','3','water vapor','0']],"remarks":"Hello 806"},\
           \
           {"questionNo":807,"questionGroup":"Air and Atmosphere","description":"On cooling, a liquid will be changed into"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','dense','0'],['0','1','solid','1'],['0','2','semi-solid','0'],['0','3','liquid','0']],"remarks":"Hello 807"},\
           \
           {"questionNo":808,"questionGroup":"Air and Atmosphere","description":"Combustion cannot take place without"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','water','0'],['0','1','carbon','0'],['0','2','air','1'],['0','3','zinc','0']],"remarks":"Hello 808"},\
           \
           {"questionNo":809,"questionGroup":"Atoms Molecules Mixtures and Compounds","description":"Remaining solid on filter paper is known as"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','solution','0'],['0','1','stone','0'],['0','2','particles','0'],['0','3','residue','1']],"remarks":"Hello 809"},\
           \
           {"questionNo":810,"questionGroup":"Atoms Molecules Mixtures and Compounds","description":"Letter used to identify an element in periodic table is known as"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','formula','0'],['0','1','idea','0'],['0','2','symbol','1'],['0','3','hint','0']],"remarks":"Hello 810"},\
           \
           {"questionNo":811,"questionGroup":"Atoms Molecules Mixtures and Compounds","description":"A component of plant cell that is absent in animal cell is known as"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','cell membrane','0'],['0','1','cytoplasm','0'],['0','2','nucleus','0'],['0','3','Cellulose','1']],"remarks":"Hello 811"},\
           \
           {"questionNo":812,"questionGroup":"Atoms Molecules Mixtures and Compounds","description":"For lowering body tube until objective is 0.25 inches of object, we use"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','illumination','0'],['0','1','Stage','0'],['0','2','diaphragm','0'],['0','3','coarse focus','1']],"remarks":"Hello 812"},\
           \
           {"questionNo":813,"questionGroup":"Atoms Molecules Mixtures and Compounds","description":"Smallest cells present in human body are"\
            ,"ques":[['0','0','0','0']],"ans":[['0','0','red blood','0'],['0','1','brain cells','1'],['0','2','egg-cell','0'],['0','3','nerve','0']],"remarks":"Hello 813"}];
            
            
            
            
    for t in testcases:
        db.session.add(QnA(questionNo=t['questionNo'], questionGroup=t['questionGroup'], description=t['description'], remarks=t['remarks'], ques=t['ques'], ans=t['ans']))
        db.session.commit()
    
