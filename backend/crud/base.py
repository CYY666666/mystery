import json
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session

from model.base import BaseModel
from utils.json_encoder import AlchemyEncoder


class CRUDBase:
    def __init__(self, model: Any):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model: BaseModel = model

    def get(self, db: Session, id: int) -> Any:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100, q=None
    ) -> Any:
        if q is None:
            q = []
        lst = db.query(self.model).filter(*q).order_by(
            self.model.create_at.desc()
        ).offset(skip).limit(limit).all()
        return json.dumps(lst, cls=AlchemyEncoder)

    def create(self, db: Session, obj_in: dict) -> Any:
        # obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Any,
        obj_in: Union[Any, Dict[str, Any]]
    ) -> Any:
        # obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Any:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def get_count(self, db: Session, q=None):
        if q is None:
            q = []
        return db.query(self.model).filter(*q).count()
