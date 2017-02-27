def insert_login(user,password,option):
    from sqlalchemy import create_engine, Column, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, scoped_session 
    
    # Base = declarative_base()
    Base = declarative_base()
    
    class User(Base):
        __tablename__ = 'user'
        id = Column(String(64), primary_key=True)
        password = Column(String(64))
        
        def __init__(self, id, password):
            """Constructor"""
            self.id = id
            self.password = password
            
        def __repr__(self):
            """Show this object (database record)"""
            return "<User(%s, %s)>" % (
            self.id, self.password)
        
    # Create a database engine
    engine = create_engine('mysql://testuser:12345678@localhost:3306/testdb')
    engine.echo = True  # Echo output to console for debugging
    
    # Drop all tables mapped in Base's subclasses
    #Base.metadata.drop_all(engine)
    
    # Create all tables mapped in Base's subclasses
    #Base.metadata.create_all(engine)
    
    # Create a database session binded to our engine, which serves as a staging area
    # for changes to the objects. To make persistent changes to database, call
    # commit(); otherwise, call rollback() to abort.
    Session = scoped_session(sessionmaker(bind=engine))
    dbsession = Session()
    
    #if(submit().option =='old_user'):
    # Insert one row via add(instance) and commit
    if(option=='new_user'):
        dbsession.add(User(user,password))
        dbsession.commit()
    elif(option=='old_user'):
        flag=0
        for instance in dbsession.query(User).filter_by(id=user).all():
            if(user==instance.id):
                if(password==instance.password):
                    flag=1
                    return flag
        else:
            return flag
                

    
    
        
    '''    
          if($op=='old_user'){
          $query="select * from User where userName='".$userName."'";
          $result = $db->query($query);
          if(!$result)
          {
              session_start();
              $_SESSION['flag']=1;
          }
          $num_results = $result->num_rows;
          $row = $result->fetch_assoc();
          if($pass==$row['Password'])
               {
                     echo "Your credentials do match!!";
                        session_start();
                        $_SESSION['flag']=0;
                        $_SESSION['pass']=$pass;
                        $_SESSION['user']=$userName;
                        header('Location: homepage.php');
                     exit;
             }
        
             else
                 {    echo "Your credentials don't match!";
                        session_start();
                        $_SESSION['flag']=1;
                        header('Location: login_signup.php');
                     exit;
                 }
          }
          
          else
          {
              
          $query="insert into User values
                    ('".$userName."', '".$pass."')";
        
        
          $result = $db->query($query);
        
          $num_results = $result->num_rows;
          session_start();
          $_SESSION['flag']=0;
          $_SESSION['pass']=$pass;
          $_SESSION['user']=$userName;
          header('Location: homepage.php');
          exit;
         }
        
          $db->close();'''
