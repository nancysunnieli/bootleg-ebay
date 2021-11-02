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

@app.route('/CreatePaymentCard', methods=['POST'])
def CreatePaymentCard():
    data = request.get_json()
    return payments_functions.CreatePaymentCard(data)


@app.route('/GetPaymentCard', methods=['GET'])
def GetPaymentCard():
    data = request.get_json()
    return payments_functions.GetPaymentCard(data['payment_id'])

@app.route('/DeleteAccount', methods=['POST'])
def DeleteAccount():
    data = request.get_json()
    return payments_functions.DeleteAccount(data['payment_id'])




if __name__ == '__main__':
    app.run(debug = True, port = 1003, host = socket.gethostbyname(socket.gethostname()))