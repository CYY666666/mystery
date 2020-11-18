
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from model import engine, Base
from model.base import BaseModel


class Answer(Base, BaseModel):
    question = Column(Text, index=True)
    choice = Column(String(16), index=True)
    subject_id = Column(Integer, index=True)
    subject_name = Column(String(64), nullable=True)

    __tablename__ = 'answer'


Base.metadata.create_all(engine)
