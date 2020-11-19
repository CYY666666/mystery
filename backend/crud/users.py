import time
from typing import List, Any, Optional
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from model import SessionLocal
from model.users import User
from utils.security import gen_password_and_salt


class CRUDAnswer(CRUDBase):
    def get_by_username(self, db: Session, username: str):
        return db.query(self.model).filter(self.model.username == username).first()

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        user.last_login_time = int(time.time())
        user.save()
        return user


user_crud = CRUDAnswer(User)


if __name__ == '__main__':
    dict_ = {
        'username': 'root',
        'remark': 'root'
    }
    info = gen_password_and_salt('666666')
    dict_.update(info)
    a: User = user_crud.create(SessionLocal(), dict_)
