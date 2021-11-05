import os
import requests
import json
import copy

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_post
from config import *

users_api = Blueprint('users', __name__)

_user_id_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'int'},
    },
    'required': ['user_id']
}

_login_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['username', 'password']
}

_none_schema = {
    'type': 'object',
    'properties': {
    },
    'required': []
}

_user_info_schema = {
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

_optional_user_info_schema = copy.deepcopy(_user_info_schema)
_optional_user_info_schema['required'] = []


@users_api.route("/user/<user_id>", methods = ['POST'])
@expects_json(_user_id_schema)
def view_user(user_id):
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/view_user")
    return get_and_post(socket_url)

@users_api.route("/login", methods = ['POST'])
@expects_json(_login_schema)
def login():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/login")
    return get_and_post(socket_url)

@users_api.route("/logout", methods = ['POST'])
@expects_json(_none_schema)
def logout():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/logout")
    return get_and_post(socket_url)

@users_api.route("/create_account", methods = ['POST'])
@expects_json(_user_info_schema)
def create_account():
    # CREATING ACCOUNT
    data_content = request.get_json()
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/create_account")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    
    new_user_info = r.content.decode('utf-8')
    
    new_user_dict = json.loads(new_user_info)
    new_user_id = new_user_dict["id"]
    
    # CREATING CART
    socket_url = ("http://" + CARTS_SERVICE_HOST + CARTS_PORT + "/create_cart")
    data_content = new_user_info
    requests.post(url = socket_url, json ={"user_id": new_user_id})
    
    return Response(response = new_user_info,
                    status = 200,
                    mimetype = 'application/json')

@users_api.route("/user/<user_id>", methods = ['POST'])
@expects_json(_user_id_schema)
def suspend_account():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/suspend_account")
    return get_and_post(socket_url)


@users_api.route("/user/<user_id>", methods = ['PUT'])
@expects_json(_optional_user_info_schema)
def modify_profile(user_id):
    dict = request.get_json()
    # TODO
    
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/modify_profile")
    return get_and_post(socket_url) 

@users_api.route("/user/<user_id>", methods = ['DELETE'])
@expects_json(_user_id_schema)
def delete_account():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/delete_account")
    return get_and_post(socket_url)