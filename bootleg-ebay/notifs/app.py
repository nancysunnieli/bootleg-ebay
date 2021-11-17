from flask import Flask, Response, request
import json
app = Flask(__name__)
import socket
import notifs_functions
from flask_expects_json import expects_json

@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')
    

@app.route('/email', methods=['POST'])
def send_email():
    data = request.get_json()
    return notifs_functions.send_email(data)

@app.route('/watchlist', methods = ['POST'])
def watchlist():
    data = request.get_json()
    auction_id = data["auction_id"]
    recipient = data["recipient"]
    return notifs_functions.watchlist_notification(recipient, auction_id)

@app.route('/seller_bid', methods = ['POST'])
def alert_seller():
    data = request.get_json()
    auction_id = data["auction_id"]
    recipient = data["recipient"]
    return notifs_functions.alert_seller_bid(recipient, auction_id)

@app.route('/buyer_bid', methods = ['POST'])
def alert_buyer():
    data = request.get_json()
    auction_id = data["auction_id"]
    recipient = data["recipient"]
    return notifs_functions.alert_buyer_bid(recipient, auction_id)

@app.route('/time', methods = ['POST'])
def time_left():
    data = request.get_json()
    auction_id = data["auction_id"]
    recipient = data["recipient"]
    time_left = data["time_left"]
    return notifs_functions.alert_before(recipient, auction_id, time_left)

@app.route('/inbox', methods = ['GET'])
def fetch_messages():
    return notifs_functions.fetch_messages()
    



if __name__ == '__main__':
    app.run(debug = True, port = 8012, host = socket.gethostbyname(socket.gethostname()), threaded=True)
