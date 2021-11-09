import os
import requests
import json
import copy

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_post, get_and_request
from config import *


users_api = Blueprint('users', __name__)

    
_user_id_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'integer'},
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


@users_api.route("/user/<user_id>", methods = ['GET'])
def view_user(user_id):
    socket_url = "http://" + USERS_SERVICE_HOST + USERS_PORT + "/user/{}".format(user_id)

    r = get_and_request(socket_url, 'get')

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@users_api.route("/login", methods = ['POST'])
@expects_json(_login_schema)
def login():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/login")
    r = get_and_request(socket_url, 'post')

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@users_api.route("/logout", methods = ['GET'])
def logout():
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/logout")
    r = get_and_request(socket_url, 'get')
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@users_api.route("/user", methods = ['POST'])
@expects_json(_user_info_schema)
def create_account():
    # create account for user

    socket_url = "http://" + USERS_SERVICE_HOST + USERS_PORT + "/user"
    r = get_and_request(socket_url, 'post')
    
    # i.e. if there's an issue with the user side
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    new_user_info = r.content.decode('utf-8')
    new_user_dict = json.loads(new_user_info)
    
    # create cart
    socket_url = ("http://" + CARTS_SERVICE_HOST + CARTS_PORT + "/create_cart")
    r = requests.post(url = socket_url, json ={"user_id": new_user_dict["id"]})
    # if not r.ok:
    #     return Response(response=r.text, status=r.status_code)
    
    return Response(response = new_user_info,
                    status = 200,
                    mimetype = 'application/json')

@users_api.route("/suspend", methods = ['PUT'])
@expects_json(_user_id_schema)
def suspend():
    socket_url = "http://" + USERS_SERVICE_HOST + USERS_PORT + "/suspend"

    r = get_and_request(socket_url, 'put')
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@users_api.route("/user/<user_id>", methods = ['PUT'])
@expects_json(_optional_user_info_schema)
def modify_profile(user_id):
    socket_url = ("http://" + USERS_SERVICE_HOST + USERS_PORT + "/user/{}".format(user_id))
    r = get_and_request(socket_url, 'put')
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@users_api.route("/user/<user_id>", methods = ['DELETE'])
@expects_json(_none_schema)
def delete_account(user_id):
    socket_url = "http://" + USERS_SERVICE_HOST + USERS_PORT + "/user/{}".format(user_id)
    r = get_and_request(socket_url, 'delete')
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content