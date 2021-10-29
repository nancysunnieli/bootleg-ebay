import requests
from flask import Flask, Response, request
import json
import socket
import os

socket_name = socket.gethostbyname(socket.gethostname())

# getting IP Address of items container
itemsServiceHost = "localhost" if os.getenv('isLocalHost') != None else "172.16.238.10"

app = Flask(__name__)

@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"},
                    status = 200,
                    mimetype = 'application/json'))


# The following functions call the items microservice

@app.route('/Items/ViewFlaggedItems', methods=['GET'])
def ViewFlaggedItems():
    socket_url = ("http://" + itemsServiceHost +
                     ":8099" + "/ViewFlaggedItems")
    r = requests.get(url = socket_url)
    return r.content

@app.route('/Items/SearchItem', methods=['POST'])
def SearchItem():
    socket_url = ("http://" +itemsServiceHost +
                     ":8099" + "/SearchItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route('/Items/AddUserToWatchlist', methods = ['POST'])
def AddUserToWarchlist():
    socket_url = ("http://" + itemsServiceHost +
                     ":8099" + "/AddUserToWatchlist")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route('/Items/RemoveItem', methods = ['POST'])
def RemoveItem():
    socket_url = ("http://" + itemsServiceHost +
                     ":8099" + "/RemoveItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route('/Items/ReportItem', methods = ['POST'])
def ReportItem():
    socket_url = ("http://" + itemsServiceHost+
                     ":8099" + "/ReportItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Items/GetItem", methods = ['POST'])
def GetItem():
    socket_url = ("http://" + itemsServiceHost +
                     ":8099" + "/GetItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Items/ModifyItem", methods = ['POST'])
def ModifyItem():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/ModifyItem")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route("/Items/AddItem", methods = ['POST'])
def AddItem():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/AddItem")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Items/EditCategories", methods = ['POST'])
def EditCategories():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/EditCategories")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


if __name__ == '__main__':
    app.run(debug = True, port = 8011, host = socket_name)
