import requests
from flask import Flask, Response, request

def get_and_post(socket_url):
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content