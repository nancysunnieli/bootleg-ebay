import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request

from utils import get_and_post
from . import routes
from config import *

# getting IP Address of users container
# The following are functions for the users microservice

UserIDSchema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'int'},
    },
    'required': ['user_id']
}

UserNamePassWordSchema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['username', 'password']
}

NoneSchema = {
    'type': 'object',
    'properties': {
    },
    'required': []
}

UserInfoSchema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'email': {'type': 'string'},
        'suspended': {'type': 'boolean'},
        'is_admin': {'type': 'boolean'}
    },
    'required': ["username", "password", "email", "suspended", "is_admin"]
}

@routes.route("/{}/ViewUser".format(USERS_NAME), methods = ['POST'])
@expects_json(UserIDSchema)
def ViewUser():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/ViewUser")
    return get_and_post(socket_url)

@routes.route("/{}/Login".format(USERS_NAME), methods = ['POST'])
@expects_json(UserNamePassWordSchema)
def Login():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/Login")
    return get_and_post(socket_url)

@routes.route("/{}/Logout".format(USERS_NAME), methods = ['POST'])
@expects_json(NoneSchema)
def Logout():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/Logout")
    return get_and_post(socket_url)

@routes.route("/{}/CreateAccount".format(USERS_NAME), methods = ['POST'])
@expects_json(UserInfoSchema)
def CreateAccount():
    # CREATING ACCOUNT
    data_content = request.get_json()
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/CreateAccount")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    
    new_user_info = r.content.decode('utf-8')
    
    new_user_dict = json.loads(new_user_info)
    new_user_id = new_user_dict["id"]
    
    # CREATING CART
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    ":3211" + "/CreateCart")
    data_content = new_user_info
    requests.post(url = socket_url, json ={"user_id": new_user_id})
    
    return Response(response = new_user_info,
                    status = 200,
                    mimetype = 'application/json')
    

    
    return new_user_info


@routes.route("/{}/SuspendAccount".format(USERS_NAME), methods = ['POST'])
@expects_json(UserIDSchema)
def SuspendAccount():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/SuspendAccount")
    return get_and_post(socket_url)


@routes.route("/{}/ModifyProfile".format(USERS_NAME), methods = ['POST'])
@expects_json(UserInfoSchema)
def ModifyProfile():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/ModifyProfile")
    return get_and_post(socket_url)

@routes.route("/{}/DeleteAccount".format(USERS_NAME), methods = ['POST'])
@expects_json(UserIDSchema)
def DeleteAccount():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/DeleteAccount")
    return get_and_post(socket_url)