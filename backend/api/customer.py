import json
import math
import time
import traceback

from flask import Blueprint, abort, make_response, jsonify
from flask import request

from api import run_in_thread, thread_executor
from crud import customer_crud
from model import SessionLocal
from model.customer import Customer
from utils.decorator import get_db
from utils.get_subject_info import get_subject_info
from utils.json_encoder import AlchemyEncoder

customer_api = Blueprint('customer', 'customer')


@customer_api.route('', methods=['POST'])
@get_db
def create_customer(db):
    data = request.get_data(as_text=True)
    try:
        json_data = json.loads(data)
        if json_data.get('got_mark', 0) < 0:
            json_data['got_mark'] = 0
        json_data['subject_name'] = get_subject_info(json_data.get('subject_id', 0))
        if not customer_crud.get_by_url(db, json_data.get('url', '')):
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
def list_customer(db):
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 20)
    try:
        data = customer_crud.get_multi(db, skip=skip, limit=limit)
        count = customer_crud.get_count(db)
        page_count = math.ceil(count / int(limit))
        return jsonify({
            'code': 0,
            'data': {
                'info': {
                    'items_count': count,
                    'page_count': page_count,
                    'per_page': int(limit)
                },
                'items': json.loads(data)
            }
        })
    except Exception as e:
        traceback.print_exc()
        abort(400)
