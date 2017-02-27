from sqlalchemy.sql.sqltypes import SMALLINT, TEXT, Integer, LargeBinary
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session 
from sqlalchemy.dialects.mssql.base import TINYINT
from sqlalchemy.sql.schema import UniqueConstraint


# Base = declarative_base()
Base = declarative_base()

class qQuestions(Base):
    __tablename__ = 'qQuestions'
    
    questionNo = Column(Integer, primary_key=True, autoincrement=True)
    courseCode = Column(String(15,collation='utf8_bin'))
    questionGroup = Column(String(32,collation='utf8_bin'))
    imgData = Column(String(128,collation='utf9_bin'))
    description = Column(TEXT(collation='utf8_bin'))
    remarks = Column (String(2048,collation='utf8_bin'))
    hasParams = Column(TINYINT)
    hasCompositeFIB = Column(TINYINT)
    hasCompositeMCMR = Column(TINYINT)
    hasCompositeSA = Column(TINYINT)


    def __init__(self,courseCode,questionGroup,description,hasParams=0,hasCompositeFIB=None,imgData=None,remarks=None,hasCompositeMCMR=None,hasCompositeSA=None,questionNo=None):
        """Constructor"""
        if questionNo:
            self.questionNo=questionNo
        self.courseCode=courseCode
        self.questionGroup=questionGroup
        self.imgData=imgData
        self.description=description
        self.remarks=remarks
        self.hasParams=hasParams
        self.hasCompositeFIB=hasCompositeFIB
        self.hasCompositeMCMR=hasCompositeMCMR
        self.hasCompositeSA=hasCompositeSA
        
    def __repr__(self):
        """Show this object (database record)"""
        return "<User(%d, %s)>" % (
        self.questionNo, self.courseCode,self.questionGroup)
        


class qAnswersMCMR(Base):
    __tablename__ = 'qAnswersMCMR'
    __table_arg__ = (UniqueConstraint("questionNo", "variationNo","answerNo","choiceNo"))
    
    questionNo = Column(Integer, autoincrement=True,primary_key=True)
    variationNo = Column(SMALLINT,primary_key=True)
    answerNo = Column(TINYINT,primary_key=True)
    choiceNo = Column(TINYINT,primary_key=True)
    choiceValue = Column(String(255))
    isAnswer = Column(TINYINT)
    canRandomize = Column(TINYINT)


    def __init__(self,questionNo,variationNo,answerNo,choiceNo,choiceValue,isAnswer=0,canRandomize=1):
        """Constructor"""
        if questionNo:
            self.questionNo=questionNo  
        self.variationNo=variationNo
        self.answerNo=answerNo
        self.choiceNo=choiceNo
        self.choiceValue=choiceValue
        self.isAnswer=isAnswer
        self.canRandomize=canRandomize

    def __repr__(self):
        """Show this object (database record)"""
        return "<User(%d, %s)>" % (
        self.questionNo, self.variationNo,self.answerNo,self.choiceNo)
    
# Create a database engine
engine = create_engine('mysql://testuser:12345678@localhost:3306/testdb')
engine.echo = True  # Echo output to console for debugging

# Drop all tables mapped in Base's subclasses
Base.metadata.drop_all(engine)

# Create all tables mapped in Base's subclasses
Base.metadata.create_all(engine)

# Create a database session binded to our engine, which serves as a staging area
# for changes to the objects. To make persistent changes to database, call
# commit(); otherwise, call rollback() to abort.
Session = scoped_session(sessionmaker(bind=engine))
dbsession = Session()

    
dbsession.add_all([qQuestions('DUM101', 'Dummies MCQ', 'Which scientist developed the theory of universal gravitation?', 0, None, None,'hello 802', None,None,802),
qQuestions('DUM101', 'Dummies MCQ', 'Which scientist created e=mc<sup>2</sup>?', 0, None,None, 'hello 803',None, None),
qQuestions('DUM101', 'Dummies MCQ', 'Which scientist explained electromagnetic induction using a concept called the lines of force?',0, None,None, 'hello 804', None, None),
qQuestions('DUM101', 'Dummies MCQ', 'How many planets are there in the solar system?',0, None, None,'hello 805', None, None),
qQuestions('DUM101', 'Dummies MCQ', 'Which planet is the closet to the Sun?',0, None,None, 'hello 806', None, None),
qQuestions('DUM101', 'Dummies MCQ', 'Which is the largest planet in our solar system?', 0, None,None,  'hello 807', None, None),
qQuestions('DUM101', 'Dummies MCQ', 'What is a sun?', 0, None, None,'hello 808',None, None)])

dbsession.add_all([qAnswersMCMR(801, 0, 0, 0, '10', False, True),
qAnswersMCMR(801, 0, 0, 1, '11', False, True),
qAnswersMCMR(801, 0, 0, 2, '2', True, True),
qAnswersMCMR(801, 0, 0, 3, '13', False, True),
qAnswersMCMR(801, 0, 0, 4, '14', False, True),
qAnswersMCMR(801, 0, 0, 5, 'None of the above', False, False),
            
qAnswersMCMR(801, 1, 0, 0, '21', False, True),
qAnswersMCMR(801, 1, 0, 1, '22', False, True),
qAnswersMCMR(801, 1, 0, 2, '23', False, True),
qAnswersMCMR(801, 1, 0, 3, '24', False, True),
qAnswersMCMR(801, 1, 0, 4, 'All of the above', False, False),
qAnswersMCMR(801, 1, 0, 5, 'None of the above', True, False),
            
qAnswersMCMR(802, 0, 0, 0, 'Issac Newtown', True, True),
qAnswersMCMR(802, 0, 0, 1, 'Charles Darwin', False, True),
qAnswersMCMR(802, 0, 0, 2, 'Albert Einstein', False, True),
qAnswersMCMR(802, 0, 0, 3, 'Michael Faraday', False, True),

qAnswersMCMR(803, 0, 0, 0, 'Issac Newtown', False, True),
qAnswersMCMR(803, 0, 0, 1, 'Charles Darwin', False, True),
qAnswersMCMR(803, 0, 0, 2, 'Albert Einstein', True, True),
qAnswersMCMR(803, 0, 0, 3, 'Michael Faraday', False, True),

qAnswersMCMR(804, 0, 0, 0, 'Issac Newtown', False, True),
qAnswersMCMR(804, 0, 0, 1, 'Charles Darwin', False, True),
qAnswersMCMR(804, 0, 0, 2, 'Albert Einstein', False, True),
qAnswersMCMR(804, 0, 0, 3, 'Michael Faraday', True, True),

qAnswersMCMR(805, 0, 0, 0, '7', False, True),
qAnswersMCMR(805, 0, 0, 1, '8', True, True),
qAnswersMCMR(805, 0, 0, 2, '9', False, True),
qAnswersMCMR(805, 0, 0, 3, '10', False, True),
qAnswersMCMR(805, 0, 0, 4, '11', False, True),
qAnswersMCMR(805, 0, 0, 5, '12', False, True),
qAnswersMCMR(805, 0, 0, 6, 'None of the above', False, False),

qAnswersMCMR(806, 0, 0, 0, 'Mercury', True, True),
qAnswersMCMR(806, 0, 0, 1, 'Saturn', False, True),
qAnswersMCMR(806, 0, 0, 2, 'Earth', False, True),
qAnswersMCMR(806, 0, 0, 3, 'Mars', False, True),
qAnswersMCMR(806, 0, 0, 4, 'Venus', False, True),
qAnswersMCMR(806, 0, 0, 5, 'Uranus', False, True),

qAnswersMCMR(807, 0, 0, 0, 'Jupiter', True, True),
qAnswersMCMR(807, 0, 0, 1, 'Saturn', False, True),
qAnswersMCMR(807, 0, 0, 2, 'Earth', False, True),
qAnswersMCMR(807, 0, 0, 3, 'Mars', False, True),
qAnswersMCMR(807, 0, 0, 4, 'Venus', False, True),
qAnswersMCMR(807, 0, 0, 5, 'Neptune', False, True),

qAnswersMCMR(808, 0, 0, 0, 'Star', True, True),
qAnswersMCMR(808, 0, 0, 1, 'Planet', False, True),
qAnswersMCMR(808, 0, 0, 2, 'Solar System', False, True),
qAnswersMCMR(808, 0, 0, 3, 'Galaxy', False, True),

qAnswersMCMR(811, 0, 0, 0, 'Mercury', True, True),
qAnswersMCMR(811, 0, 0, 1, 'Moon', False, True),
qAnswersMCMR(811, 0, 0, 2, 'Jupiter', True, True),
qAnswersMCMR(811, 0, 0, 3, 'Pluto', False, True),
qAnswersMCMR(811, 0, 0, 4, 'Mars', True, True),
            
qAnswersMCMR(812, 0, 0, 0, 'Hydrogen', True, True),
qAnswersMCMR(812, 0, 0, 1, 'Oxygen', True, True),
qAnswersMCMR(812, 0, 0, 2, 'Chlorine', False, True),
qAnswersMCMR(812, 0, 0, 3, 'Carbon', False, True),

qAnswersMCMR(813, 0, 0, 0, 'Steve Jobs', True, True),
qAnswersMCMR(813, 0, 0, 1, 'Adam & Eve', True, True),
qAnswersMCMR(813, 0, 0, 2, 'Newton', True, True),
qAnswersMCMR(813, 0, 0, 3, 'All of the above', True, False),

qAnswersMCMR(814, 0, 0, 0, 'Red', True, True),
qAnswersMCMR(814, 0, 0, 1, 'Green', True, True),
qAnswersMCMR(814, 0, 0, 2, 'Blue', True, True),
qAnswersMCMR(814, 0, 0, 3, 'All of the above', True, False),
qAnswersMCMR(814, 0, 0, 4, 'None of the above', False, False),

qAnswersMCMR(815, 0, 0, 0, 'Definite shape', True, True),
qAnswersMCMR(815, 0, 0, 1, 'Definite volume', True, True),
qAnswersMCMR(815, 0, 0, 2, 'Indefinite shape', False, True),
qAnswersMCMR(815, 0, 0, 3, 'Indefinite volume', False, True),

qAnswersMCMR(816, 0, 0, 0, 'Definite shape', False, True),
qAnswersMCMR(816, 0, 0, 1, 'Definite volume', True, True),
qAnswersMCMR(816, 0, 0, 2, 'Indefinite shape', True, True),
qAnswersMCMR(816, 0, 0, 3, 'Indefinite volume', False, True),

qAnswersMCMR(817, 0, 0, 0, 'Definite shape', False, True),
qAnswersMCMR(817, 0, 0, 1, 'Definite volume', False, True),
qAnswersMCMR(817, 0, 0, 2, 'Indefinite shape', True, True),
qAnswersMCMR(817, 0, 0, 3, 'Indefinite volume', True, True),

qAnswersMCMR(851, 0, 0, 0, 'to control the current flowing thru the LED', True, True),
qAnswersMCMR(851, 0, 0, 1, 'to waste power', False, True),
qAnswersMCMR(851, 0, 0, 2, 'to look good', False, True),
qAnswersMCMR(851, 0, 0, 3, "I don't know", True, True),

qAnswersMCMR(851, 1, 0, 0, 'to control the current flowing thru the LED', True, True),
qAnswersMCMR(851, 1, 0, 1, 'to waste power', False, True),
qAnswersMCMR(851, 1, 0, 2, 'to look good', False, True),
qAnswersMCMR(851, 1, 0, 3, "I don't know", True, True),

qAnswersMCMR(851, 2, 0, 0, 'to control the current flowing thru the LED', True, True),
qAnswersMCMR(851, 2, 0, 1, 'to waste power', False, True),
qAnswersMCMR(851, 2, 0, 2, 'to look good', False, True),
qAnswersMCMR(851, 2, 0, 3, "I don't know", True, True),

qAnswersMCMR(851, 0, 1, 0, '7.9 mA', True, True),
qAnswersMCMR(851, 0, 1, 1, '0 mA', False, True),
qAnswersMCMR(851, 0, 1, 2, '15 mA', False, True),
qAnswersMCMR(851, 0, 1, 3, '5 mA', False, True),
            
qAnswersMCMR(851, 1, 1, 0, '9.6 mA', True, True),
qAnswersMCMR(851, 1, 1, 1, '0 mA', False, True),
qAnswersMCMR(851, 1, 1, 2, '15 mA', False, True),
qAnswersMCMR(851, 1, 1, 3, '5 mA', False, True),
            
qAnswersMCMR(851, 2, 1, 0, '0 mA', True, True),
qAnswersMCMR(851, 2, 1, 1, '5 mA', False, True),
qAnswersMCMR(851, 2, 1, 2, '15 mA', False, True),
qAnswersMCMR(851, 2, 1, 3, '10 mA', False, True),

qAnswersMCMR(851, 0, 5, 0, 'True', False, True),
qAnswersMCMR(851, 0, 5, 1, 'False', True, True),

qAnswersMCMR(851, 1, 5, 0, 'True', False, True),
qAnswersMCMR(851, 1, 5, 1, 'False', True, True),

qAnswersMCMR(851, 2, 5, 0, 'True', False, True),
qAnswersMCMR(851, 2, 5, 1, 'False', True, True)])

dbsession.commit()

ques=dbsession.query(qQuestions).all()
ans=dbsession.query(qAnswersMCMR).all()

#for instance in ques:
    #   print(instance.questionNo, instance.questionGroup, instance.description)
