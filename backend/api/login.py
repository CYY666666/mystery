import json
from datetime import timedelta
from typing import Any

from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, create_refresh_token

import config
import crud
from utils import security
from utils.decorator import get_db

login_api = Blueprint('login', 'login')


@login_api.route("/access-token", methods=['POST'])
@get_db
def login_access_token(db) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    data = request.get_data(as_text=True)
    json_data = json.loads(data)
    user = crud.user_crud.authenticate(
        db, username=json_data.get('username'), password=json_data.get('password')
    )
    if not user:
        abort(400)
    elif not crud.user_crud.is_active(user):
        abort(400)
    access_token = create_access_token(identity=user.id, fresh=True, expires_delta=timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(user.id, expires_delta=timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
