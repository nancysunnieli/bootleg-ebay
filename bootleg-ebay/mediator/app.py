import requests
from flask import Flask, Response, request
import json
import socket

socket_name = socket.gethostbyname(socket.gethostname())

app = Flask(__name__)

@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"},
                    status = 200,
                    mimetype = 'application/json'))


# The following functions call the items microservice

@app.route('/ViewFlaggedItems', methods=['GET'])
def ViewFlaggedItems():
    socket_url = ("http://" + socket_name +
                     ":8099" + "/ViewFlaggedItems")
    r = requests.get(url = socket_url)
    return r.content

@app.route('/SearchItem', methods=['POST'])
def SearchItem():
    socket_url = ("http://" + socket_name +
                     ":8099" + "/SearchItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route('/AddUserToWatchlist', methods = ['POST'])
def AddUserToWarchlist():
    socket_url = ("http://" + socket_name +
                     ":8099" + "/AddUserToWatchlist")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route('/RemoveItem', methods = ['POST'])
def RemoveItem():
    socket_url = ("http://" + socket_name +
                     ":8099" + "/RemoveItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route('/ReportItem', methods = ['POST'])
def ReportItem():
    socket_url = ("http://" + socket_name +
                     ":8099" + "/ReportItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/GetItem", methods = ['POST'])
def GetItem():
    socket_url = ("http://" + socket_name +
                     ":8099" + "/GetItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/ModifyItem", methods = ['POST'])
def ModifyItem():
    socket_url = ("http://" + socket_name +
                    ":8099" + "/ModifyItem")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route("/AddItem", methods = ['POST'])
def AddItem():
    socket_url = ("http://" + socket_name +
                    ":8099" + "/AddItem")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/EditCategories", methods = ['POST'])
def EditCategories():
    socket_url = ("http://" + socket_name +
                    ":8099" + "/EditCategories")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


if __name__ == '__main__':
    app.run(debug = True, port = 8098, host = socket_name)