from typing import List, Any
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from model import SessionLocal
from model.answer import Answer


class CRUDAnswer(CRUDBase):

    def get_answer_by_question_subject_id(
        self, db: Session, question: str, subject_id: int
    ) -> Answer:
        return (
            db.query(self.model)
            .filter(self.model.question == question, self.model.subject_id == subject_id)
            .first()
        )

    def create_or_update(self, db: Session, obj_in: dict):
        question = obj_in.get('question')
        subject_id = obj_in.get('subject_id')
        answer = self.get_answer_by_question_subject_id(db, question, subject_id)
        if not answer:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        else:
            answer.choice = obj_in.get('choice')
            db.commit()
            db.refresh(answer)
        return


answer_crud = CRUDAnswer(Answer)


if __name__ == '__main__':
    a: Answer = answer_crud.get_answer_by_question_subject_id(SessionLocal(), '台湾问题的核心是', 7)
    print(a.choice)
