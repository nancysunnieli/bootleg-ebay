import json
import socket

from flask import Flask, Response, request, jsonify


import payments_functions
from payments import APIError

app = Flask(__name__)


@app.errorhandler(500)
def handle_exception(err):
    """Return JSON instead of HTML for server error"""
    response = {"error": str(err)}
    return jsonify(response), 500

@app.errorhandler(APIError)
def handle_api_error(err):
    """Return custom JSON when APIError"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
        
    return jsonify(response), err.code

@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')

@app.route('/card', methods=['POST'])
def create_payment_card():
    data = request.get_json()
    return payments_functions.create_payment_card(data)


@app.route('/card/<payment_id>', methods=['GET'])
def get_payment_card(payment_id):
    return payments_functions.get_payment_card(payment_id)

@app.route('/card_by_user/<user_id>', methods=['GET'])
def get_payment_card_by_user_id(user_id):
    return payments_functions.get_payment_card_by_user_id(user_id)

@app.route('/card/<payment_id>', methods=['DELETE'])
def delete_payment_card(payment_id):
    return payments_functions.delete_payment_card(payment_id)

@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    return payments_functions.create_transaction(data)

@app.route('/transaction/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    return payments_functions.get_transaction(transaction_id)

@app.route('/transactions_by_user_id/<user_id>', methods=['GET'])
def get_transactions_by_user_id(user_id):
    return payments_functions.get_transactions_by_user_id(user_id)

@app.route('/transaction/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    return payments_functions.delete_transaction(transaction_id)



if __name__ == '__main__':
    app.run(debug = True, port = 1003, host = socket.gethostbyname(socket.gethostname()))