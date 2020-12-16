import json
from datetime import timedelta
from typing import Any

from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, fresh_jwt_required

import config
import crud
from crud import user_crud
from model.users import User
from utils import security
from utils.decorator import get_db

user_api = Blueprint('user', 'user')


@user_api.route("/reset_password", methods=['POST'])
@fresh_jwt_required
@get_db
def reset_password(db) -> Any:
    data = request.get_data(as_text=True)
    json_data = json.loads(data)
    user = crud.user_crud.reset_password(
        db, user_id=get_jwt_identity(), password=json_data.get('password')
    )
    return "success"


@user_api.route("/get_users", methods=['GET'])
@fresh_jwt_required
@get_db
def get_users(db) -> Any:
    user_id = get_jwt_identity()
    user: User = user_crud.get(db, user_id)
    q = [User.id == user_id] if not user_crud.is_superuser(user) else None
    data = user_crud.get_multi(db, skip=0, limit=100, q=q)
    data = json.loads(data)
    return {'data': data}
