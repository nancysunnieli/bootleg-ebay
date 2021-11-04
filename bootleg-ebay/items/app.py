from flask import Flask, Response, request
import json
app = Flask(__name__)
import item_functions
import socket

@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')

@app.route('/ViewAllItems', methods = ['POST'])
def ViewAllItems():
    data = request.get_json()
    if "limit" in data:
        limit = data["limit"]
    else:
        limit = None
    return item_functions.ViewAllItems(limit)

@app.route('/ViewFlaggedItems', methods=['GET'])
def ViewFlaggedItems():
    return item_functions.ViewFlaggedItems()

@app.route('/SearchItem', methods=['POST'])
def SearchItem():
    data = request.get_json()
    keywords = data["keywords"]
    return item_functions.SearchItem(keywords)

@app.route('/AddUserToWatchlist', methods = ['POST'])
def AddUserToWarchlist():
    data = request.get_json()
    id = data["item_id"]
    user_id = data["user_id"]
    return item_functions.AddUserToWatchlist(id, user_id)

@app.route('/RemoveItem', methods = ['POST'])
def RemoveItem():
    data = request.get_json()
    id = data["item_id"]
    return item_functions.RemoveItem(id)

@app.route('/ReportItem', methods = ['POST'])
def ReportItem():
    data = request.get_json()
    item = data["item_id"]
    reason = data["reason"]
    return item_functions.ReportItem(item, reason)

@app.route("/GetItem", methods = ['POST'])
def GetItem():
    data = request.get_json()
    item = data["item_id"]
    return item_functions.GetItem(item)

@app.route("/ModifyItem", methods = ['POST'])
def ModifyItem():
    data = request.get_json()
    id = data["item_id"]

    if "name" in data:
        name = data["name"]
    else:
        name = None

    if "description" in data:
        description = data["description"]
    else:
        description = None
    
    if "category" in data:
        category = data["category"]
    else:
        category = None
    
    if "photos" in data:
        photos = data["photos"]
    else:
        photos = None
    
    if "price" in data:
        price = data["price"]
    else:
        price = None

    return item_functions.ModifyItem(id, name,
                                    description, 
                                    category, photos, 
                                    price)

@app.route("/AddItem", methods = ['POST'])
def AddItem():
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    category = data["category"]
    photos = data["photos"]
    sellerID = data["sellerID"]
    price = data["price"]

    return item_functions.AddItem(name, description, category,
                                photos, sellerID, price)

@app.route("/EditCategories", methods = ['POST'])
def EditCategories():
    data = request.get_json()
    id = data["item_id"]
    category = data["category"]
    return item_functions.EditCategories(id, category)

@app.route("/ModifyAvailability", methods = ['POST'])
def ModifyAvailability():
    data = request.get_json()
    id = data["item_id"]
    return item_functions.ModifyAvailability(id)


if __name__ == '__main__':
    app.run(debug = True, port = 8099, host = socket.gethostbyname(socket.gethostname()))