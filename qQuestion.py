from sqlalchemy.sql.sqltypes import SMALLINT, TEXT, Integer, LargeBinary
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session 
from sqlalchemy.dialects.mssql.base import TINYINT
from MySQLdb.constants.FIELD_TYPE import VARCHAR
from sqlalchemy.sql.schema import PrimaryKeyConstraint
    
def qQuestions(): 
    
    # Base = declarative_base()
    Base = declarative_base()
    
    class qQuestions(Base):
        __tablename__ = 'qQuestions'
        
        questionNo = Column(Integer, primary_key=True, autoincrement=True)
        courseCode = Column(String(15),collation='utf8')
        questionGroup = Column(String(32),collation='utf8')
        imgData = Column(LargeBinary)
        description = Column(TEXT,collation='utf8')
        remarks = Column (String(2048),collation='utf8')
        hasParams = Column(TINYINT(1))
        hasCompositeFIB = Column(TINYINT(1))
        hasCompositeMCMR = Column(TINYINT(1))
        hasCompositeSA = Column(TINYINT(1))


        def __init__(self,questionNo=None,courseCode,questionGroup,imgData=None,description,remarks=None,hasParams=0,hasCompositeFIB=None,hasCompositeMCMR=None,hasCompositeSA=None):
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
        
    # Create a database engine
    engine = create_engine('mysql://testuser:12345678@localhost:3306/testdb')
    engine.echo = True  # Echo output to console for debugging
    
    # Drop all tables mapped in Base's subclasses
    #Base.metadata.drop_all(engine)
    
    # Create all tables mapped in Base's subclasses
    Base.metadata.create_all(engine)
    
    # Create a database session binded to our engine, which serves as a staging area
    # for changes to the objects. To make persistent changes to database, call
    # commit(); otherwise, call rollback() to abort.
    Session = scoped_session(sessionmaker(bind=engine))
    dbsession = Session()


def qAnswersMCMR():

    
    # Base = declarative_base()
    Base = declarative_base()
    
    class qAnswersMCMR(Base):
        __tablename__ = 'qAnswersMCMR'
        
        questionNo = Column(Integer(10), primary_key=True, autoincrement=True)
        variationNo = Column(SMALLINT(5), primary_key=True)
        answerNo = Column(TINYINT(3),primary_key=True)
        choiceNo = Column(TINYINT(3), primary_key=True)
        choiceValue = Column(VARCHAR(256),collation='utf8')
        isAnswer = Column (TINYINT(1))
        canRandomize = Column(TINYINT(1))


        def __init__(self,questionNo,variationNo,answerNo,choiceNo,choiceValue,isAnswer=0,canRandomize=1):
            """Constructor"""
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
    #Base.metadata.drop_all(engine)
    
    # Create all tables mapped in Base's subclasses
    Base.metadata.create_all(engine)
    
    # Create a database session binded to our engine, which serves as a staging area
    # for changes to the objects. To make persistent changes to database, call
    # commit(); otherwise, call rollback() to abort.
    Session = scoped_session(sessionmaker(bind=engine))
    dbsession = Session()
   

