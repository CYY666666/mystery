import functools

from model import SessionLocal


def get_db(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with SessionLocal() as db:
            return func(db, *args, **kwargs)

    return wrapper
