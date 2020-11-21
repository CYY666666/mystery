import hashlib
import os
import secrets
from datetime import timedelta, datetime
from typing import Union, Any

from passlib.context import CryptContext
from jose import jwt

import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def gen_password_and_salt(password_text):
    """ 生成加密后的密码和盐 """
    salt = os.urandom(32)
    dk = hashlib.pbkdf2_hmac(
        config.PASSWORD_HASH_FUNC_NAME,
        password_text.encode('utf-8'),
        salt,
        config.PASSWORD_HASH_ITERATIONS,
    )
    return {'password': dk, 'salt': salt}


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
