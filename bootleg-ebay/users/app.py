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

@app.route('/ViewUser', methods=['POST'])
def ViewUser():
    data = request.get_json()
    user_id = data["user_id"]
    return users_functions.ViewUser(user_id)

@app.route('/Login', methods=['POST'])
def Login():
    data = request.get_json()
    username = data["username"]
    password = data['password']
    return users_functions.Login(username, password)

@app.route('/Logout', methods=['POST'])
def Logout():
    return users_functions.Logout()

@app.route('/CreateAccount', methods=['POST'])
def CreateAccount():
    data = request.get_json()
    return users_functions.CreateAccount(data)

@app.route('/SuspendAccount', methods=['POST'])
def SuspendAccount():
    data = request.get_json()
    user_id = data["user_id"]
    return users_functions.SuspendAccount(user_id)

@app.route('/ModifyProfile', methods=['POST'])
def ModifyProfile():
    data = request.get_json()
    return users_functions.ModifyProfile(data)

@app.route('/DeleteAccount', methods=['POST'])
def DeleteAccount():
    data = request.get_json()
    user_id = data["user_id"]
    return users_functions.DeleteAccount(user_id)



if __name__ == '__main__':
    app.run(debug = True, port = 3306, host = socket.gethostbyname(socket.gethostname()))