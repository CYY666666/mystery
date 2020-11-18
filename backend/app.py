import asyncio

from flask import Flask
from flask_cors import *

from api.customer import customer_api
from api.info import info_api
from celery_core.celery_app import make_celery

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
app.register_blueprint(customer_api, url_prefix='/api/customer')
app.register_blueprint(info_api, url_prefix='/api/info')
celery = make_celery(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
