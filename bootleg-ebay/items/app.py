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

@app.route('/view_all_items', methods = ['POST'])
def view_all_items():
    data = request.get_json()
    if not data:
        data = {}
    if "limit" in data:
        limit = data["limit"]
    else:
        limit = None
    return item_functions.view_all_items(limit)

@app.route('/view_flagged_items', methods=['POST'])
def view_flagged_items():
    data = request.get_json()
    if not data:
        data = {}
    if "limit" in data:
        limit = data["limit"]
    else:
        limit = None
    return item_functions.view_flagged_items(limit)

@app.route('/search_item', methods=['POST'])
def search_item():
    data = request.get_json()
    keywords = data["keywords"]
    return item_functions.search_item(keywords)

@app.route('/add_user_to_watch_list', methods = ['POST'])
def add_user_to_watch_list():
    data = request.get_json()
    id = data["item_id"]
    user_id = data["user_id"]
    return item_functions.add_user_to_watch_list(id, user_id)

@app.route('/remove_item', methods = ['POST'])
def remove_item():
    data = request.get_json()
    id = data["item_id"]
    return item_functions.remove_item(id)

@app.route('/report_item', methods = ['POST'])
def report_item():
    data = request.get_json()
    item = data["item_id"]
    reason = data["reason"]
    return item_functions.report_item(item, reason)

@app.route("/get_item", methods = ['POST'])
def get_item():
    data = request.get_json()
    item = data["item_id"]
    return item_functions.get_item(item)

@app.route("/modify_item", methods = ['POST'])
def modify_item():
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

    return item_functions.modify_item(id, name,
                                    description, 
                                    category, photos, 
                                    price)

@app.route("/add_item", methods = ['POST'])
def add_item():
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    category = data["category"]
    photos = data["photos"]
    sellerID = data["sellerID"]
    price = data["price"]

    return item_functions.add_item(name, description, category,
                                photos, sellerID, price)

@app.route("/edit_categories", methods = ['POST'])
def edit_categories():
    data = request.get_json()
    id = data["item_id"]
    category = data["category"]
    return item_functions.edit_categories(id, category)

@app.route("/modify_availability", methods = ['POST'])
def modify_availability():
    data = request.get_json()
    id = data["item_id"]
    return item_functions.modify_availability(id)


if __name__ == '__main__':
    # Don't set host as localhost, otherwise it wont be reachable through docker networks
    # Should run this file with docker-compose up, and talk to it via localhost:8011 on your system
    app.run(debug = True, port = 8099, host = "localhost")
    #app.run(debug = True, port = 8099, host = socket.gethostbyname(socket.gethostname()))