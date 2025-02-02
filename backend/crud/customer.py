import json
from datetime import date, timedelta, datetime
from typing import List, Any
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from model import SessionLocal
from model.customer import Customer
from utils.date import get_before_today_start_timestamp, get_before_today_end_timestamp
from utils.json_encoder import AlchemyEncoder


class CRUDCustomer(CRUDBase):
    def create(self, db: Session, obj_in: dict) -> Any:
        # obj_in_data = jsonable_encoder(obj_in)
        obj_in['daily_got_mark'] = {}
        for i in range(0, obj_in['days']):
            obj_in['daily_got_mark'][str(date.today() + timedelta(days=i))] = 0
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_got_mark(self, db: Session, id: int):
        db_obj: Customer = self.get(db, id)
        db_obj.got_mark += 1
        db_obj.real_total_mark += 1
        d = str(date.today())
        temp = db_obj.daily_got_mark.copy()
        if temp.get(d, None) is None:
            temp[d] = 0
        temp[d] += 1
        db_obj.daily_got_mark = temp
        db.commit()
        db.refresh(db_obj)
        return True

    def minus_got_mark(self, db: Session, id: int):
        db_obj: Customer = self.get(db, id)
        db_obj.got_mark -= 1
        db_obj.real_total_mark -= 1
        d = str(date.today())
        temp = db_obj.daily_got_mark.copy()
        if temp.get(d, None) is None:
            temp[d] = 0
        temp[d] -= 1
        db_obj.daily_got_mark = temp
        db.commit()
        db.refresh(db_obj)
        return True
    
    def set_real_accuracy(self, db: Session, id: int, accuracy: float):
        db_obj: Customer = self.get(db, id)
        db_obj.real_accuracy = accuracy
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

    def set_days(self, db: Session, days):
        lst = db.query(self.model).filter(
            self.model.days == 1,
            # self.model.create_at >= 1668355200,
            # self.model.create_at < 1668355200
        ).all()
        for item in lst:
            if item.got_mark:
                # for i in range(0, int(days)):
                    # print('str(date.today() - timedelta(days=1) + timedelta(days=i))', str(date.today() - timedelta(days=1) + timedelta(days=i)))
                    # print('item.daily_got_mark,', item.daily_got_mark)
                if item.daily_got_mark is None:
                    item.daily_got_mark = {}
                temp = item.daily_got_mark.copy()
                # if i == 0:
                temp = {str(date.today()): item.total_mark}
                    # else:
                    #     temp[str(date.today() + timedelta(days=i))] = 0
                    # else:

                    # temp['2022-11-15'] = 0
                    # temp['2022-11-16'] = 0
                    # temp['2022-11-17'] = 0
                item.daily_got_mark = temp
        db.commit()
        return json.dumps(lst, cls=AlchemyEncoder)

    def create_daily_task(self, db: Session):
        ids = []
        for i in range(1, 6):
            lst = db.query(self.model).filter(
                self.model.days >= max(2, i),
                self.model.create_at >= get_before_today_start_timestamp(i),
                self.model.create_at < get_before_today_end_timestamp(i)
            ).all()
            for item in lst:
                if item.daily_got_mark.get(str(date.today()),
                                           0) < item.total_mark and item.real_total_mark < item.total_mark * item.days:
                    # print('id: ', item.id)
                    # print('daily_got_mark: ', item.daily_got_mark)
                    # print('daily_got_mark: ', item.daily_got_mark.get(str(date.today()), 0))
                    # print('total_mark: ', item.total_mark)
                    # print('real_total_mark: ', item.real_total_mark)
                    # print('days: ', item.days)
                    item.got_mark = item.total_mark - min(item.total_mark,
                                                          item.days * item.total_mark - item.real_total_mark)
                    ids.append(item.id)
            db.commit()
            from celery_core.crawler import crawler
            for item in lst:
                crawler.delay(item.id)
        return ids

    def create_daily_task2(self, db: Session):
        ids = []
        for i in range(1, 5):
            lst = db.query(self.model).filter(
                self.model.days >= max(2, i),
                self.model.create_at >= get_before_today_start_timestamp(i),
                self.model.create_at < get_before_today_end_timestamp(i)
            ).all()
            for item in lst:
                if item.daily_got_mark.get(str(date.today()), 0) + item.daily_got_mark.get(str(date.today() - timedelta(days=1)), 0) < item.total_mark * 2 and item.real_total_mark < item.total_mark * item.days:
                    # print('id: ', item.id)
                    # print('daily_got_mark: ', item.daily_got_mark)
                    # print('daily_got_mark: ', item.daily_got_mark.get(str(date.today()), 0))
                    # print('total_mark: ', item.total_mark)
                    # print('real_total_mark: ', item.real_total_mark)
                    # print('days: ', item.days)
                    item.got_mark = item.total_mark - min(item.total_mark,
                                                          2 * item.total_mark - item.daily_got_mark.get(str(date.today()), 0) + item.daily_got_mark.get(str(date.today() - timedelta(days=1)), 0))
                    ids.append(item.id)
            db.commit()
            from celery_core.crawler import crawler
            for item in ids:
                crawler.delay(item)
        return ids

    def query_daily_task(self, db: Session):
        ids = []
        for i in range(1, 5):
            lst = db.query(self.model).filter(
                self.model.days >= max(2, i),
                self.model.create_at >= get_before_today_start_timestamp(i),
                self.model.create_at < get_before_today_end_timestamp(i)
            ).all()
            for item in lst:
                if item.daily_got_mark.get(str(date.today()), 0) < item.total_mark and item.real_total_mark < item.total_mark * item.days:
                    # print('id: ', item.id)
                    # print('daily_got_mark: ', item.daily_got_mark)
                    # print('daily_got_mark: ', item.daily_got_mark.get(str(date.today()), 0))
                    # print('total_mark: ', item.total_mark)
                    # print('real_total_mark: ', item.real_total_mark)
                    # print('days: ', item.days)
                    # item.got_mark = item.total_mark - min(item.total_mark, item.days * item.total_mark - item.real_total_mark)
                    ids.append(item.id)
            # db.commit()
            # from celery_core.crawler import crawler
            # for item in lst:
            #     crawler.delay(item.id)
        return ids


customer_crud = CRUDCustomer(Customer)
