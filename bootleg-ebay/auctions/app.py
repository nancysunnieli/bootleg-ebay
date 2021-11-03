import json
import socket

from flask import Flask, Response, request


import auctions_functions

app = Flask(__name__)
socket_name = socket.gethostbyname(socket.gethostname())

@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')


@app.route('/CreateAuction', methods=['POST'])
def CreateAuction():
    data = request.get_json()
    return auctions_functions.CreateAuction(data)

@app.route('/GetAuction', methods=['POST'])
def GetAuction():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.GetAuction(auction_id)

@app.route('/ViewCurrentAuctions', methods=['POST'])
def ViewCurrentAuctions():
    return auctions_functions.ViewCurrentAuctions()

@app.route('/RemoveAuction', methods=['POST'])
def RemoveAuction():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.RemoveAuction(auction_id)

@app.route('/CompleteAuction', methods=['POST'])
def CompleteAuction():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.CompleteAuction(auction_id)


@app.route('/BidsByUser', methods=['POST'])
def BidsByUser():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.BidsByUser(auction_id, data['buyer_id'])

@app.route('/CreateBid', methods=['POST'])
def CreateBid():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.CreateBid(auction_id, data['price'], data['buyer_id'])

@app.route('/ViewBids', methods=['POST'])
def ViewBids():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.ViewBids(auction_id)

@app.route('/BuyNow', methods=['POST'])
def BuyNow():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.BuyNow(auction_id, data['buyer_id'])

if __name__ == '__main__':
    app.run(debug = True, port = 2222, host = socket_name)