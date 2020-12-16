import json
import math
import time
import traceback

from flask import Blueprint, abort, make_response, jsonify
from flask import request
from flask_jwt_extended import fresh_jwt_required, get_jwt_identity

from api import run_in_thread, thread_executor
from crud import customer_crud, user_crud
from model import SessionLocal
from model.customer import Customer
from model.users import User
from utils.decorator import get_db
from utils.get_subject_info import get_subject_info
from utils.json_encoder import AlchemyEncoder

customer_api = Blueprint('customer', 'customer')


@customer_api.route('', methods=['POST'])
@get_db
@fresh_jwt_required
def create_customer(db):
    data = request.get_data(as_text=True)
    try:
        json_data = json.loads(data)
        if json_data.get('got_mark', 0) < 0:
            json_data['got_mark'] = 0
        json_data['user_id'] = get_jwt_identity()
        json_data['subject_name'] = get_subject_info(json_data.get('subject_id', 0))
        if not customer_crud.get_by_url_subject_id(db, json_data.get('url', ''), json_data.get('subject_id'), user_id=get_jwt_identity()):
            custom: Customer = customer_crud.create(db, json_data)
            from celery_core.crawler import crawler
            crawler.delay(custom.id)
            return jsonify({
                'code': 0,
                'data': json.loads(json.dumps(custom, cls=AlchemyEncoder))
            })
        else:
            abort(400)
    except Exception as e:
        traceback.print_exc()
        abort(400)


@customer_api.route('/restart_task', methods=['POST'])
@get_db
@fresh_jwt_required
def restart_task(db):
    data = request.get_data(as_text=True)
    try:
        json_data = json.loads(data)
        customer_id_list = json_data.get('customer_id_list')
        from celery_core.crawler import crawler
        for customer_id in customer_id_list:
            crawler.delay(customer_id)

        return '成功'
    except Exception as e:
        traceback.print_exc()
        abort(400)


@customer_api.route('', methods=['GET'])
@get_db
@fresh_jwt_required
def list_customer(db):
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 20)
    user_id_param = request.args.get('user_id', None)
    try:
        user_id = get_jwt_identity()
        user: User = user_crud.get(db, user_id)
        q = [Customer.user_id == user_id] if not user_crud.is_superuser(user) else \
            [Customer.user_id == user_id_param] if user_id_param else None
        data = customer_crud.get_multi(db, skip=skip, limit=limit, q=q)
        data = json.loads(data)
        for i in data:
            create_user: User = user_crud.get(db, i['user_id'])
            username = create_user.remark if create_user else None
            i['username'] = username
        count = customer_crud.get_count(db, q)
        page_count = math.ceil(count / int(limit))
        return jsonify({
            'code': 0,
            'data': {
                'info': {
                    'items_count': count,
                    'page_count': page_count,
                    'per_page': int(limit)
                },
                'items': data
            }
        })
    except Exception as e:
        traceback.print_exc()
        abort(400)
