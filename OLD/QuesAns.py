from sqlalchemy.sql.sqltypes import SMALLINT, TEXT, Integer, LargeBinary, FLOAT
from sqlalchemy import create_engine, Column, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session 
from sqlalchemy.dialects.mssql.base import TINYINT
from MySQLdb.constants.FIELD_TYPE import VARCHAR
from sqlalchemy.sql.schema import UniqueConstraint, PrimaryKeyConstraint,\
    ForeignKeyConstraint, ForeignKey
    
# Base = declarative_base()
Base = declarative_base()

class qQuestions(Base):
    __tablename__ = 'qQuestions'
    
    questionNo = Column(Integer, primary_key=True, autoincrement=True)
    courseCode = Column(String(15,collation='utf8_general_ci'))
    questionGroup = Column(String(32,collation='utf8_general_ci'))
    imgData = Column(LargeBinary)
    description = Column(TEXT(collation='utf8_general_ci'))
    remarks = Column (String(2048,collation='utf8_general_ci'))
    hasParams = Column(SMALLINT)
    hasCompositeFIB = Column(SMALLINT)
    hasCompositeMCMR = Column(SMALLINT)
    hasCompositeSA = Column(SMALLINT)
    
    def __init__(self,courseCode,questionGroup,description,questionNo=None,imgData=None,remarks=None,hasParams=0,hasCompositeFIB=None,hasCompositeMCMR=None,hasCompositeSA=None):
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
        
class qQuestionImageParams(qQuestions):
    tablename = 'qQuestionImageParams'
    paramNo = Column(SMALLINT)
    posX = Column(FLOAT)
    posY = Column(FLOAT)
    
    def __init__(self,paramNo,posX=None,posY=None):
        self.paramNo=paramNo
        self.posX=posX
        self.posY=posY
        
    def __repr__(self):
        return "<User(%d, %s)>" % (
        self.questionNo, self.paramNo,self.posX,self.posY)
        
class qQuestionSpecs(qQuestions):
    questionType = Column(Enum('MC','MR','FIB','SA', name='quesType'), nullable = False)
    maxMarks = Column(SMALLINT)
    numQuestions = Column(SMALLINT, nullable = False)
    #remarks = Column(String(2048,collation = 'utf8_general_ci'))
    
    def __init__(self,questionType,maxMarks=1,numQuestions=0,remarks=None):
        self.questionType=questionType
        self.maxMarks=maxMarks
        self.numQuestions=numQuestions
        self.remarks=remarks
        
    def __repr__(self):
        return "<User(%d, %s)>" % (
        self.courseCode, self.questionGroup,self.questionType,self.maxMarks,self.numQuestions)
        
    
    

class qQuestionParts(qQuestions):
    tablename = 'qQuestionParts'
    partNo = Column(SMALLINT, nullable= False)
    partType = Column(Enum('MC', 'MR', 'FIB', 'SA', name='partType'), nullable= False)
    partDesc = Column(TEXT(collation='utf8_general_ci'), nullable= False)
    partMarks = Column(SMALLINT, nullable= False)
    
    def __init__(self,partNo,partType,partDesc,partMarks=1):
        self.partNo=partNo
        self.partType=partType
        self.Desc=partDesc
        self.partMarks=partMarks
        
    def __repr__(self):
        return "<User(%d, %s)>" % (
        self.questionNo,self.partNo, self.partType,self.Desc,self.partMarks)
                    
        
class qAnswers(Base):
    __tablename__ = 'qAnswers'
    __table_arg__ = (UniqueConstraint("questionNo", "variationNo","answerNo"))
    
    questionNo = Column(Integer, autoincrement=True,primary_key=True)
    variationNo = Column(SMALLINT,primary_key=True)
    answerNo = Column(TINYINT,primary_key=True)
    
    PrimaryKeyConstraint('questionNo','variationNo','answerNo', name='ansPK')


    def __init__(self,questionNo,variationNo,answerNo,choiceNo,choiceValue,isAnswer=0,canRandomize=1):
        """Constructor"""
        if questionNo:
            self.questionNo=questionNo  
        self.variationNo=variationNo
        self.answerNo=answerNo

    def __repr__(self):
        """Show this object (database record)"""
        return "<User(%d, %s)>" % (
        self.questionNo, self.variationNo,self.answerNo)
        
class qAnswersMCMR(qAnswers):
    __tablename__ = 'qAnswersMCMR'
    quesNo=Column(Integer, primary_key=True)
    varNo = Column(SMALLINT, primary_key=True)
    ansNo = Column(TINYINT, primary_key=True)
    choiceValue = Column(String(255))
    isAnswer = Column(TINYINT)
    canRandomize = Column(TINYINT)
    
    ForeignKeyConstraint([quesNo,varNo,ansNo],[qAnswers.questionNo,qAnswers.variationNo,qAnswers.answerNo])

    def __init__(self,choiceValue,isAnswer=0,canRandomize=1):
        """Constructor"""
        
        self.choiceValue=choiceValue
        self.isAnswer=isAnswer
        self.canRandomize=canRandomize

    def __repr__(self):
        """Show this object (database record)"""
        return "<User(%d, %s)>" % (
        self.questionNo, self.variationNo,self.answerNo,self.choiceValue)
        
#class qAnswerMC(qAnswersMCMR):   #FUTURE CLASS-SPECIFIC FUNCTIONS
#class qAnswerMR(qAnswersMCMR):      
        
class qAnswersFIB(qAnswers):
    tablename = 'qAnswersFIB'
    quesNo=Column(Integer, primary_key=True)
    varNo = Column(SMALLINT, primary_key=True)
    ansNo = Column(TINYINT, primary_key=True)
    answerValue = Column(String(256,collation='utf8_general_ci'))
    FIBTolerance = Column(SMALLINT)
    FIBStringCS = Column(TINYINT)
    
    ForeignKeyConstraint([quesNo,varNo,ansNo],[qAnswers.questionNo,qAnswers.variationNo,qAnswers.answerNo])
    
    def __init__(self,answerValue,FIBTolerance=0,FIBStringCS=0):
        """Constructor"""
        
        self.answerValue=answerValue
        self.FIBTolerance=FIBTolerance
        self.FIBStringCS=FIBStringCS

    def __repr__(self):
        """Show this object (database record)"""
        return "<User(%d, %s)>" % (
        self.questionNo, self.variationNo,self.answerNo,self.answerValue)
    
class qAnswersSA(qAnswers):
    tablename = 'qAnswersSA'
    
    #questionNo=Column(Integer, ForeignKey('qAnswers.questionNo'), primary_key=True)
    answerKeys = Column(String(512,collation='utf8_general_ci'))
    
    def __init__(self,answerKeys=None):
        """Constructor"""
        
        self.answerKeys=answerKeys

    def __repr__(self):
        """Show this object (database record)"""
        return "<User(%d, %s)>" % (
        self.questionNo, self.variationNo,self.answerNo,self.answerKeys)
        
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

"""    
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
qAnswersMCMR(851, 2, 5, 1, 'False', True, True)])"""

dbsession.commit()

ques=dbsession.query(qQuestions).all()
ans=dbsession.query(qAnswersMCMR).all()

#for instance in ques:
    #   print(instance.questionNo, instance.questionGroup, instance.description)