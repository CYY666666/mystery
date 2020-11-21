import json
from datetime import timedelta
from typing import Any

from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, fresh_jwt_required

import config
import crud
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
