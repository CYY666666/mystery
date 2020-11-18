import time

from sqlalchemy import Column, BigInteger, Integer


class BaseModel:
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_at = Column(BigInteger, index=True, default=time.time)
    delete_at = Column(BigInteger, index=True, default=-1)
