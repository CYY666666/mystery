FROM python:3.8-slim-buster

RUN mkdir /qmyz-backend
WORKDIR /qmyz-backend
COPY ./requirements.txt /qmyz-backend/requirements.txt

RUN pip install psycopg2-binary
RUN pip install -r requirements.txt
COPY . /qmyz-backend
ENV FLASK_APP=app.py

EXPOSE 5000

CMD flask run --host=0.0.0.0
