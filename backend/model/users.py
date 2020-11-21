
from sqlalchemy import Column, Integer, String, Text, Binary, BigInteger, Boolean

from model import engine, Base
from model.base import BaseModel


class User(Base, BaseModel):
    username = Column(String(16), index=True)
    remark = Column(String(16), index=True)
    password = Column(Binary)
    salt = Column(Binary)
    state = Column(Integer, index=True, default=50)
    last_login = Column(BigInteger, index=True, default=-1)
    is_superuser = Column(Boolean, default=False)

    __tablename__ = 'users'


Base.metadata.create_all(engine)
