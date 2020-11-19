import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from config import *


def connect(user, password, db, host=DB_URL, port=DB_PORT):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    engine = sqlalchemy.create_engine(url, client_encoding='utf8', pool_size=10, pool_pre_ping=True)

    return engine


class MySession(Session):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class MySessionMaker(sessionmaker):
    def __init__(
            self,
            bind=None,
            class_=MySession,
            autoflush=True,
            autocommit=False,
            expire_on_commit=True,
            info=None,
            **kw
    ):
        kw["bind"] = bind
        kw["autoflush"] = autoflush
        kw["autocommit"] = autocommit
        kw["expire_on_commit"] = expire_on_commit
        if info is not None:
            kw["info"] = info
        self.kw = kw
        # make our own subclass of the given class, so that
        # events can be associated with it specifically.
        self.class_ = type(class_.__name__, (class_,), {})


engine = connect(DB_USER, DB_PASSWORD, DB)
Base = declarative_base()
SessionLocal = MySessionMaker(autocommit=False, autoflush=False, bind=engine)
