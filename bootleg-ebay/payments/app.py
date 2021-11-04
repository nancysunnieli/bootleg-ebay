import json
import socket

from flask import Flask, Response, request


import payments_functions

app = Flask(__name__)


@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')

@app.route('/create_payment_card', methods=['POST'])
def create_payment_card():
    data = request.get_json()
    return payments_functions.create_payment_card(data)


@app.route('/get_payment_card', methods=['GET'])
def get_payment_card():
    data = request.get_json()
    return payments_functions.get_payment_card(data['payment_id'])

@app.route('/delete_account', methods=['POST'])
def delete_account():
    data = request.get_json()
    return payments_functions.delete_account(data['payment_id'])




if __name__ == '__main__':
    app.run(debug = True, port = 1003, host = socket.gethostbyname(socket.gethostname()))