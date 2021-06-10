import time

from sqlalchemy import Column, Integer, String, Text, Boolean

from model import engine, Base
from model.base import BaseModel


class Customer(Base, BaseModel):
    url = Column(Text, index=True)
    remark = Column(String(16), index=True)
    subject_id = Column(Integer, index=True)
    subject_name = Column(String(64), nullable=True)
    total_mark = Column(Integer, index=True)
    got_mark = Column(Integer, index=True, default=0)
    accuracy = Column(Integer, index=True, default=80)
    user_id = Column(Integer, index=True, nullable=True)
    is_paid = Column(Boolean, index=True, nullable=True, default=False)

    __tablename__ = 'customer'


Base.metadata.create_all(engine)
