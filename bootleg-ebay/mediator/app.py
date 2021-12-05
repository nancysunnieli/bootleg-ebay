import requests
import json
import socket
import os

from flask import Flask, Response, request
from flask_expects_json import expects_json
from flask_cors import CORS, cross_origin
from celery import Celery

from routes import *

app = Flask(__name__)
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(payments_api, url_prefix='/payments')
app.register_blueprint(auctions_api, url_prefix='/auctions')
app.register_blueprint(carts_api, url_prefix='/carts')
app.register_blueprint(items_api, url_prefix='/items')
app.register_blueprint(notifs_api, url_prefix='/notifs')

socket_name = socket.gethostbyname(socket.gethostname())


CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

broker_url = "amqp://rabbitmq-server"
celery = Celery(app.name, broker=broker_url, include=['celery_tasks.auctions'])
app.celery = celery


@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')

# @app.after_request
# def after_request(response):
# #   response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
# #   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   response.headers.add('Access-Control-Allow-Credentials', 'true')
#   return response


if __name__ == '__main__':
    app.run(debug = True, port = 8011, host = socket_name, threaded=True)
