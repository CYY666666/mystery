import traceback

import requests
import re
import time
import json

from app import celery
from crud import customer_crud, answer_crud
from model.customer import Customer
from utils.decorator import get_db, get_db_celery


@celery.task()
@get_db_celery
def crawler(db, customer_id: int):
    p = r'\w+'  # 匹配answer
    pattern = re.compile(p)
    with celery.app.app_context():
        customer = customer_crud.get(db, customer_id)
        url = customer.url
        subject_id = customer.subject_id
        total_mark = customer.total_mark
        accuracy = customer.accuracy
        got_mark = customer.got_mark
        headers_1 = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; vivo x6s a Build/LYZ28N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 yiban_android',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'qm.linyisong.top',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        response_1 = requests.post(url=url, headers=headers_1)
        cookies = response_1.cookies.get_dict()
        headers_2 = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; vivo x6s a Build/LYZ28N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 yiban_android',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'qm.linyisong.top',
            'Cookie': 'JSESSIONID=' + cookies['JSESSIONID'] + '; Path=/yiban-web; HttpOnly',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }

        response_2 = requests.post(url=url, headers=headers_2)
        cookie = 'JSESSIONID=' + cookies['JSESSIONID']
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; vivo x6s a Build/LYZ28N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 yiban_android',
            'Host': 'qm.linyisong.top',
            'Origin': 'http://qm.linyisong.top',
            'Referer': 'http://qm.linyisong.top/yiban-web/stu/toSubject.jhtml?courseId=7',
            'Cookie': cookie,
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        question_url = 'http://qm.linyisong.top/yiban-web/stu/nextSubject.jhtml?_=1549905749917'
        choice_url = 'http://qm.linyisong.top/yiban-web/stu/changeSituation.jhtml?_=1545318034464'

        total_tmp = 1
        now_ = 0
        try:
            while got_mark < total_mark:
                response = requests.post(url=question_url, data={'courseId': subject_id}, headers=headers)
                question_json = response.json()
                uuid = question_json.get('data', {}).get('uuid', '')
                question = question_json.get('data', {}).get('nextSubject', {}).get('subDescript', '')
                answer = answer_crud.get_answer_by_question_subject_id(db, question, subject_id)
                if answer:
                    choice = answer.choice
                else:
                    choice = 'A'
                if (now_ / total_tmp * 100) > accuracy:
                    choice = 'A'
                response2 = requests.post(url=choice_url,
                                          data={'answer': choice, 'courseId': subject_id, 'uuid': uuid},
                                          headers=headers)

                answer_json = response2.json()
                is_true = answer_json.get('data', {}).get('rightAnswer', None)

                if is_true:
                    true_choice = choice
                    now_ += 1
                    customer_crud.add_got_mark(db, customer_id)
                else:
                    right_option = answer_json.get('data', {}).get('rightOption', '')
                    matcher2 = re.search(pattern, right_option)
                    true_choice = matcher2.group(0)
                    customer_crud.minus_got_mark(db, customer_id)
                data = {
                    'question': question,
                    'choice': true_choice,
                    'subject_id': subject_id
                }
                answer_crud.create_if_not_exist(db, data)
                got_mark = customer.got_mark
                total_tmp += 1
                time.sleep(6)

        except Exception as e:
            traceback.print_exc()
            time.sleep(10)
