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


@routes.route("/{}/CreateAuction".format(auctionsName), methods = ['POST'])
def CreateAuction():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/CreateAuction")
    return get_and_post(socket_url)

@routes.route("/{}/GetAuction".format(auctionsName), methods = ['POST'])
def GetAuction():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/GetAuction")
    return get_and_post(socket_url)

@routes.route("/{}/ViewCurrentAuctions".format(auctionsName), methods = ['POST'])
def ViewCurrentAuctions():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/ViewCurrentAuctions")
    return get_and_post(socket_url)

@routes.route("/{}/RemoveAuction".format(auctionsName), methods = ['POST'])
def RemoveAuction():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/RemoveAuction")
    return get_and_post(socket_url)

@routes.route("/{}/BidsByUser".format(auctionsName), methods = ['POST'])
def BidsByUser():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/BidsByUser")
    return get_and_post(socket_url)

@routes.route("/{}/CreateBid".format(auctionsName), methods = ['POST'])
def CreateBid():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/CreateBid")
    return get_and_post(socket_url)

@routes.route("/{}/ViewBids".format(auctionsName), methods = ['POST'])
def ViewBids():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/ViewBids")
    return get_and_post(socket_url)
