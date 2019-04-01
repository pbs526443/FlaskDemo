'''

'''

class Text():
    def __init__(self):
        self.id = id

class Book():
    id = None
    name = None
    price = None

    def __str__(self):
        return "id:%s name: %s price %s"% (self.id,self.name,self.price)


from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                                    encoding='utf8', echo=True)
from  sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(bind=engine)
from sqlalchemy import Column,Integer,String,ForeignKey
class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    username = Column(String(20),nullable=False)
    password = Column(String(20),nullable=False)

class Books(Base):
    __tablename__ = "books"
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    bookname = Column(String(20),nullable=True)
    price = Column(String(20),nullable=True)

class Memorandum(Base):
    __tablename__ = "memorandum"
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    memorname = Column(String(20),nullable=False)
    memorcontent = Column(String(150),nullable=False)
    userid = Column(Integer,ForeignKey("user.id"),nullable=False)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
