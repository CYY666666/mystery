import time
from typing import List, Any, Optional
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from model import SessionLocal
from model.users import User
from utils.security import gen_password_and_salt, verify_password, get_password_hash


class CRUDAnswer(CRUDBase):
    def create(self, db: Session, obj_in: dict) -> User:
        db_obj = User(
            username=obj_in.get('username'),
            password=bytes(get_password_hash(obj_in.get('password')), encoding='utf-8'),
            remark=obj_in.get('remark'),
            state=obj_in.get('state'),
            is_superuser=obj_in.get('is_superuser'),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_username(self, db: Session, username: str):
        return db.query(self.model).filter(self.model.username == username).first()

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        user.last_login = int(time.time())
        db.commit()
        db.refresh(user)
        return user

    def is_active(self, user: User) -> bool:
        return user.state == 50

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def reset_password(self, db, user_id: int, password: str):
        user: User = self.get(db, user_id)
        user.password = bytes(get_password_hash(password), encoding='utf-8')
        db.commit()
        db.refresh(user)
        return user


user_crud = CRUDAnswer(User)


if __name__ == '__main__':
    pass
