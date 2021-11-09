import json
import socket

from flask import Flask, Response, request, jsonify


import users_functions
from users import APIError

app = Flask(__name__)


@app.errorhandler(500)
def handle_exception(err):
    """Return JSON instead of HTML for server error"""
    # app.logger.error(f"Unknown Exception: {str(err)}")
    # app.logger.debug(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
    response = {"error": str(err)}
    return jsonify(response), 500

@app.errorhandler(APIError)
def handle_api_error(err):
    """Return custom JSON when APIError"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
        
    # Add some logging so that we can monitor different types of errors 
    # app.logger.error(f"{err.description}: {response["message"]}")
    return jsonify(response), err.code

@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')

@app.route('/user/<user_id>', methods=['GET'])
def view_user(user_id):
    # data = request.get_json()
    # user_id = data["user_id"]
    return users_functions.view_user(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data["username"]
    password = data['password']
    return users_functions.login(username, password)

@app.route('/logout', methods=['GET'])
def logout():
    return users_functions.logout()

@app.route('/user', methods=['POST'])
def create_account():
    data = request.get_json()
    return users_functions.create_account(data)

@app.route('/suspend', methods=['PUT'])
def suspend():
    data = request.get_json()
    user_id = data["user_id"]
    return users_functions.suspend(user_id)

@app.route('/user/<user_id>', methods=['PUT'])
def modify_profile(user_id):
    data = request.get_json()
    data['user_id'] = user_id
    return users_functions.modify_profile(data)

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_account(user_id):
    # data = request.get_json()
    # user_id = data["user_id"]
    return users_functions.delete_account(user_id)



if __name__ == '__main__':
    app.run(debug = True, port = 1001, host = socket.gethostbyname(socket.gethostname()))