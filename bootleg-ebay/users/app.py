import json
import socket

from flask import Flask, Response, request


import users_functions

app = Flask(__name__)


@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')

@app.route('/view_user', methods=['GET'])
def view_user():
    data = request.get_json()
    user_id = data["user_id"]
    return users_functions.view_user(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data["username"]
    password = data['password']
    return users_functions.login(username, password)

@app.route('/logout', methods=['POST'])
def logout():
    return users_functions.logout()

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    return users_functions.create_account(data)

@app.route('/suspend_account', methods=['POST'])
def suspend_account():
    data = request.get_json()
    user_id = data["user_id"]
    return users_functions.suspend_account(user_id)

@app.route('/modify_profile', methods=['POST'])
def modify_profile():
    data = request.get_json()
    return users_functions.modify_profile(data)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    data = request.get_json()
    user_id = data["user_id"]
    return users_functions.delete_account(user_id)



if __name__ == '__main__':
    app.run(debug = True, port = 1001, host = socket.gethostbyname(socket.gethostname()))