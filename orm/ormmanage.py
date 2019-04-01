from orm import model
from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                                    encoding='utf8', echo=True)
from sqlalchemy.orm import sessionmaker
session = sessionmaker()()
def inserUser(username,password):
    try:
        result = session.add(model.User(username=username,password=password))
        session.commit()
        print(result)
    except Exception as e:
        print(e)
    finally:
        session.close()

def checkUser(username,password):
    try:
        result = session.query(model.User).filter(model.User.username == username).filter(model.User.password == password).first()
        if result:
            return result
        else:
            return -1
    except Exception as e:
        print(e)
    finally:
        session.close()

def inserBooks(bookname,price):
    try:
        print(bookname,price)
        result = session.add(model.Books(bookname=bookname,price=price))
        session.commit()
        print(result,"<---------")
    except Exception as e:
        print(e)
    finally:
        session.close()

def checkBooks():
    try:
        result = session.query(model.Books.id,model.Books.bookname,model.Books.price).all()
        if result:
            return result
        else:
            return -1
    except Exception as e:
        print(e)
    finally:
        session.close()

def deleteBooks(id):
    try:
        result = session.query(model.Books).filter(model.Books.id == id).delete()
        session.commit()
        print(result)
    except Exception as e:
        print(e)
    finally:
        session.close()

def insertmemor(memorname,memorcontent,userid):
    try:
        result = session.add(model.Memorandum(memorname=memorname,memorcontent=memorcontent,userid=userid))
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()

def checkmemor(id):
    try:
        result = session.query(model.Memorandum.id,model.Memorandum.memorname,model.Memorandum.memorcontent).filter(model.Memorandum.userid == id).all()
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(e)
    finally:
        session.close()

def checkmemor1(id):
    try:
        result = session.query(model.Memorandum.memorname,model.Memorandum.memorcontent).filter(model.Memorandum.id == id).all()
        if result:
            return result
        else:
            return -1
    except Exception as e:
        print(e)
    finally:
        session.close()


def deletememor(id):
    try:
        result = session.query(model.Memorandum).filter(model.Memorandum.id == id).delete()
        session.commit()
        print(result)
    except Exception as e:
        print(e)
    finally:
        session.close()

def updatememor(id,memorname,memorcontent):
    try:
        # session.query(model.Memorandum).filter(model.Memorandum.id == id).first().memorname=memorname
        # session.commit()
        # result = session.query(model.Memorandum).filter(model.Memorandum.id == id).first().memorcontent=memorcontent
        # session.commit()
        result = session.query(model.Memorandum).filter(model.Memorandum.id == id).update({"memorname":memorname,"memorcontent":memorcontent})
        session.commit()
        return result
    except Exception as e:
        print(e)
    finally:
        session.close