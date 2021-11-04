import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_post
from config import *

# getting IP Address of auctions container
# The following are functions for the auctions microservice

auctions_api = Blueprint('auctions', __name__)


@auctions_api.route("/{}/create_auction".format(AUCTIONS_NAME), methods = ['POST'])
def create_auction():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/create_auction")
    return get_and_post(socket_url)

@auctions_api.route("/{}/get_auction".format(AUCTIONS_NAME), methods = ['POST'])
def get_auction():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/get_auction")
    return get_and_post(socket_url)

@auctions_api.route("/{}/view_current_auctions".format(AUCTIONS_NAME), methods = ['POST'])
def view_current_auctions():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/view_current_auctions")
    return get_and_post(socket_url)

@auctions_api.route("/{}/remove_auction".format(AUCTIONS_NAME), methods = ['POST'])
def remove_auction():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/remove_auction")
    return get_and_post(socket_url)

@auctions_api.route("/{}/bids_by_user".format(AUCTIONS_NAME), methods = ['POST'])
def bids_by_user():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/bids_by_user")
    return get_and_post(socket_url)

@auctions_api.route("/{}/create_bid".format(AUCTIONS_NAME), methods = ['POST'])
def create_bid():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/create_bid")
    return get_and_post(socket_url)

@auctions_api.route("/{}/view_bids".format(AUCTIONS_NAME), methods = ['POST'])
def view_bids():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/view_bids")
    return get_and_post(socket_url)
