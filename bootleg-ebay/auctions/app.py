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


@app.route('/create_auction', methods=['POST'])
def create_auction():
    data = request.get_json()
    return auctions_functions.create_auction(data)

@app.route('/get_auction', methods=['POST'])
def get_auction():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.get_auction(auction_id)

@app.route('/view_current_auctions', methods=['POST'])
def view_current_auctions():
    return auctions_functions.view_current_auctions()

@app.route('/remove_auction', methods=['POST'])
def remove_auction():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.remove_auction(auction_id)


@app.route('/bids_by_user', methods=['POST'])
def bids_by_user():
    data = request.get_json()
    return auctions_functions.bids_by_user(data['buyer_id'])

@app.route('/create_bid', methods=['POST'])
def create_bid():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.create_bid(auction_id, data['price'], data['buyer_id'])

@app.route('/view_bids', methods=['POST'])
def view_bids():
    data = request.get_json()
    auction_id = data['_id']
    return auctions_functions.view_bids(auction_id)

if __name__ == '__main__':
    app.run(debug = True, port = 2222, host = socket_name)