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

@app.route('/Email', methods=['POST'])
@expects_json(EmailPostSchema)
def SendEmail():
    data = request.get_json()
    return notifs_functions.SendEmail(data)

if __name__ == '__main__':
    app.run(debug = True, port = 8012, host = socket.gethostbyname(socket.gethostname()))