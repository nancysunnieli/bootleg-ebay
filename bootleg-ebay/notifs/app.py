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
    
EmailPostSchema = {
    'type': 'object',
    'properties': {
        'recipient': {'type': 'string',  "minLength": 1},
        'subject': {'type': 'string'},
        'body': {'type': 'string'},
    },
    'required': ['recipient', 'subject', 'body']
}

RecipientItem= {
    'type': 'object',
    'properties': {
        'recipient' : {'type': 'string'},
        'item_id' : {'type' : 'string'},
    },
    'required': ['recipient', 'item_id']
}

Time= {
    'type': 'object',
    'properties': {
        'recipient' : {'type': 'string'},
        'item_id' : {'type' : 'string'},
        'time_left' : {'type' : 'string'},
    },
    'required': ['recipient', 'item_id', 'time_left']
}

@app.route('/email', methods=['POST'])
@expects_json(EmailPostSchema)
def SendEmail():
    data = request.get_json()
    return notifs_functions.SendEmail(data)

@app.route('/watchlist', methods = ['POST'])
@expects_json(RecipientItem)
def watchlist():
    data = request.get_json()
    item_id = data["item_id"]
    recipient = data["recipient"]
    return notifs_functions.watchlist_notification(recipient, item_id)

@app.route('/seller_bid')
@expects_json(RecipientItem)
def alert_seller():
    data = request.get_json()
    item_id = data["item_id"]
    recipient = data["recipient"]
    return notifs_functions.alert_seller_bid(recipient, item_id)

@app.route('/buyer_bid')
@expects_json(RecipientItem)
def alert_seller():
    data = request.get_json()
    item_id = data["item_id"]
    recipient = data["recipient"]
    return notifs_functions.alert_buyer_bid(recipient, item_id)

@app.route('/time')
@expects_json(Time)
def time_left():
    data = request.get_json()
    item_id = data["item_id"]
    recipient = data["recipient"]
    time_left = data["time_left"]
    return notifs_functions.alert_buyer_bid(recipient, item_id, time_left)



if __name__ == '__main__':
    app.run(debug = True, port = 8012, host = socket.gethostbyname(socket.gethostname()))
