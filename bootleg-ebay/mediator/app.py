import requests
import json
import socket
import os

from flask import Flask, Response, request
from flask_expects_json import expects_json
from flask_cors import CORS

from routes import *

app = Flask(__name__)
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(payments_api, url_prefix='/payments')
app.register_blueprint(auctions_api, url_prefix='/auctions')
app.register_blueprint(items_api, url_prefix='/items')
app.register_blueprint(carts_api, url_prefix='/carts')



socket_name = socket.gethostbyname(socket.gethostname())


CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')



if __name__ == '__main__':
    app.run(debug = True, port = 8011, host = socket_name)
