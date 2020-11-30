
from flask import Blueprint, jsonify
from flask_jwt_extended import fresh_jwt_required

from utils.get_subject_info import subject_dict

info_api = Blueprint('info', 'info')


@info_api.route('', methods=['GET'])
@fresh_jwt_required
def get_info():
    return jsonify(subject_dict)
