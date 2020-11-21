import functools

from requests import Session

from model import SessionLocal, engine, MySessionMaker


def get_db(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with SessionLocal() as db:
            return func(db, *args, **kwargs)

    return wrapper


def get_db_celery(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        engine.dispose()
        with engine.connect() as conn:
            SessionLocalCelery = MySessionMaker(autocommit=False, autoflush=False, bind=conn)
            with SessionLocalCelery() as db:
                return func(db, *args, **kwargs)

    return wrapper
