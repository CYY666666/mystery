import asyncio

from flask import Flask
from flask_cors import *
from flask_jwt_extended import JWTManager

from api.customer import customer_api
from api.info import info_api
from api.login import login_api
from api.user import user_api
from celery_core.celery_app import make_celery
from config import SECRET_KEY

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
app.register_blueprint(customer_api, url_prefix='/api/customer')
app.register_blueprint(info_api, url_prefix='/api/info')
app.register_blueprint(login_api, url_prefix='/api/login')
app.register_blueprint(user_api, url_prefix='/api/user')
celery = make_celery(app)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager()
jwt.init_app(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
