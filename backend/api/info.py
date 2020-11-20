
from flask import Blueprint, jsonify

info_api = Blueprint('info', 'info')


@info_api.route('', methods=['GET'])
def get_info():
    data = {
        2: '形势与政策',
        7: '毛泽东思想和中国特色社会主义理论体系概论',
        8: '思想道德修养与法律基础',
        9: '马克思主义基本原理',
        10: '中国近代史纲要',
        12: '学习新思想',
        15: '社会主义先进文化',
        16: '不忘初心',
        19: '70周年',
        68: '学习四史'
    }
    return jsonify(data)
