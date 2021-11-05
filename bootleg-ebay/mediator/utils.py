import requests
from flask import Flask, Response, request

def get_and_post(socket_url):
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


def get_and_request(socket_url, request_type):

    request_dict = {
        'post': requests.post,
        'get': requests.get,
        'put': requests.put,
        'delete': requests.delete
    }

    data_content = request.get_json()
    r = request_dict[request_type](url = socket_url, json = data_content)
    return r
