import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request

from utils import get_and_post
from . import routes
from config import *

# getting IP Address of auctions container
# The following are functions for the auctions microservice


@routes.route("/{}/CreateAuction".format(AUCTIONS_NAME), methods = ['POST'])
def CreateAuction():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/CreateAuction")
    return get_and_post(socket_url)

@routes.route("/{}/GetAuction".format(AUCTIONS_NAME), methods = ['POST'])
def GetAuction():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/GetAuction")
    return get_and_post(socket_url)

@routes.route("/{}/ViewCurrentAuctions".format(AUCTIONS_NAME), methods = ['POST'])
def ViewCurrentAuctions():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/ViewCurrentAuctions")
    return get_and_post(socket_url)

@routes.route("/{}/RemoveAuction".format(AUCTIONS_NAME), methods = ['POST'])
def RemoveAuction():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/RemoveAuction")
    return get_and_post(socket_url)

@routes.route("/{}/BidsByUser".format(AUCTIONS_NAME), methods = ['POST'])
def BidsByUser():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/BidsByUser")
    return get_and_post(socket_url)

@routes.route("/{}/CreateBid".format(AUCTIONS_NAME), methods = ['POST'])
def CreateBid():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/CreateBid")
    return get_and_post(socket_url)

@routes.route("/{}/ViewBids".format(AUCTIONS_NAME), methods = ['POST'])
def ViewBids():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/ViewBids")
    return get_and_post(socket_url)
