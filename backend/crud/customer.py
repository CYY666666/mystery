from typing import List, Any
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from model import SessionLocal
from model.customer import Customer


class CRUDCustomer(CRUDBase):
    def add_got_mark(self, db: Session, id: int):
        db_obj: Customer = self.get(db, id)
        db_obj.got_mark += 1
        db.commit()
        db.refresh(db_obj)
        return True

    def minus_got_mark(self, db: Session, id: int):
        db_obj: Customer = self.get(db, id)
        db_obj.got_mark -= 1
        db.commit()
        db.refresh(db_obj)
        return True

    def get_got_mark(self, db: Session, id: int) -> int:
        db_obj: Customer = self.get(db, id)
        return db_obj.got_mark

    def get_by_url_subject_id(self, db: Session, url: str, subject_id: int, user_id: int):
        return db.query(self.model).filter(
            self.model.url == url,
            self.model.subject_id == subject_id,
            self.model.user_id == user_id
        ).first()


customer_crud = CRUDCustomer(Customer)
