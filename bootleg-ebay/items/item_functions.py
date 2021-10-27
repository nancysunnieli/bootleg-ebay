import pymongo
from pymongo import MongoClient
import csv
import uuid
from items import Item
import re


client = pymongo.MongoClient("mongodb://root:bootleg@localhost:27017")
db = client["items"]
items_collection = db["items"]
flagged_items_collection = db["flagged_items"]
photos_collection = db["photos"]


def generate_random_id():
    return str(uuid.uuid4())[:12]

def reformat_list_csv(array):
    """
    CSV format messes up arrays, so I have to reformat it
    """
    result = array.split(",")
    for i in range(0, len(result)):
        result[i] = re.sub("[\[\]]", "", result[i])
        result[i] = result[i].replace("'", "")
    return result

def create_photos_database(data_file_path, collection = photos_collection):
    file = open(data_file_path)
    csvreader = csv.reader(file)
    all_entries = []
    for row in csvreader:
        photo = {"_id": None, "photo": None}
        photo["_id"] = row[0]
        photo["photo"] = row[1]
        all_entries.append(photo)
    file.close()
    collection.insert_many(all_entries)
    
def create_flagged_items_database(data_file_path, collection = flagged_items_collection):
    file = open(data_file_path)
    csvreader = csv.reader(file)
    all_entries = []
    for row in csvreader:
        flagged_item = {"_id": None, "itemID": None, "FlagReason": None}
        flagged_item["_id"] = row[0]
        flagged_item["itemID"] = row[1]
        flagged_item["FlagReason"] = row[2]
        all_entries.append(flagged_item)
    file.close()
    collection.insert_many(all_entries)


def create_items_database(data_file_path, collection = items_collection):
    """
    This creates the items database in mongo db with
    the fake data in the mock_data folder.

    Schema for items: id, name, description,
            category, photos, sellerID,
            price, isFlagged
    """

    file = open(data_file_path)
    csvreader = csv.reader(file)
    all_items = []
    for row in csvreader:
        item = {"_id": None, "name": None, "description": None,
                "category": None, "photos": None, "sellerID": None,
                "price": None, "isFlagged": None}
        item["_id"] = row[0]
        item["name"] = row[1]
        item["description"] = row[2]
        item["category"] = reformat_list_csv(row[3])
        item["photos"] = row[4]
        item["sellerID"] = row[5]
        item["price"] = row[6]
        item["isFlagged"] = row[7]
        watchlist = reformat_list_csv(row[8])
        item["watchlist"] = watchlist

        all_items.append(item)
    file.close()
    

    collection.insert_many(all_items)

def create_all_databases(items_data_file_path, flagged_items_data_file_path,
                        photos_data_file_path, item_collection = items_collection, 
                        flagged_item_collection = flagged_items_collection,
                        photo_collection = photos_collection):
    """
    This creates all the collections in our microservice
    """
    create_items_database(items_data_file_path, item_collection)
    create_flagged_items_database(flagged_items_data_file_path, flagged_item_collection)
    create_photos_database(photos_data_file_path, photo_collection)



def ViewFlaggedItems(limit = None, collection = items_collection):
    """
    This returns all the flagged items
    """
    query = {"isFlagged": "True"}
    results = list(collection.find(query))
    if limit:
        return results[:limit]
    else:
        return results

def EditCategories(item_id, updated_categories, collection = items_collection):
    query = { "_id" : item_id }
    new_categories = { "$set": { "category": updated_categories } }
    result = collection.update_one(query, new_categories)

    if result.modified_count > 0:
        return "Change was Successful!"
    else:
        return "Change was not Successful. Please Try Again."

def AddItem(id, name, description, category, photos, 
                sellerID, price, isFlagged, watchlist,
                collection = items_collection):
    """
    This adds one item to our database
    """
    item = {"_id": None, "name": None, "description": None,
                "category": None, "photos": None, "sellerID": None,
                "price": None, "isFlagged": None, "watchlist": None}
    item["_id"] = id
    item["name"] = name
    item["description"] = description
    item["category"] = category
    item["photos"] = photos
    item["sellerID"] = sellerID
    item["price"] = price
    item["isFlagged"] = isFlagged
    item["watchlist"] = watchlist
    result = collection.insert_one(item)

    if len(list(collection.find({ "_id": id}))) == 1:
        return "Item Successfully Inserted!"
    else:
        return "Item was not successfully inserted. Please Try Again."



def ModifyItem(id, name = None, description = None,
                category = None, photos = None, price = None,
                collection = items_collection):
    """
    With this function, I can modify the item
    that matches the given id.

    I can modify the name, description, category,
    photos, and price
    """
    query = { "_id" : id }
    modifications = []
    if name:
        new_name = { "$set": { "name": name } }
        modifications.append(new_name)
    if description:
        new_description = { "$set": { "description": description } }
        modifications.append(new_description)
    if category:
        new_categories = { "$set": { "category": category } }
        modifications.append(new_categories)
    if photos:
        new_photos = { "$set": { "photos": photos } }
        modifications.append(new_photos)
    if price:
        new_price = { "$set": { "price": price } }
        modifications.append(new_price)

    success = []
    failure = []
    for modification in modifications:
        result = collection.update_one(query, modification)
        if result.modified_count > 0:
            for key, value in modification["$set"].items():
                success.append(key)
        else:
            for key, value in modification["$set"].items():
                failure.append(key)

    string_to_return = ""
    if len(success) > 0:
        string_to_return += ("Successfully changed %s fields" % ", ".join(success))
    if len(failure) > 0:
        if string_to_return != "":
            string_to_return += " "
        string_to_return += ("Failure to change %s fields." % ", ".join(failure))
    return string_to_return

def GetItem(id, collection = items_collection):
    """
    given an item id, this function returns back the item
    """
    query = {"_id": id}
    results = list(collection.find(query))
    return results

def AddFlaggedItem(id, item_id, flag_reason, collection = flagged_items_collection):
    """
    This adds a new flag to the database
    """
    item = {"_id": id, "itemID": item_id, "FlaggedReason": flag_reason}
    collection.insert_one(item)

    if len(list(collection.find({"_id" : id}))) == 1:
        return "Flag Successfully Added!"
    else:
        return "Flag Failure. Please Try Again."


def ReportItem(id, flag_reason, item_collection = items_collection, 
                flagged_item_collection = flagged_items_collection):
    """
    This flags an item, and gives the flag reason
    """
    # updates item database
    query = {"_id": id}
    flag = {"$set" : {"isFlagged" : "True" }}
    update_result = item_collection.update_one(query, flag)

    
    # updates flagged items database
    flag_id = generate_random_id()
    result = AddFlaggedItem(flag_id, id, flag_reason)
    if (result == "Flag Successfully Added!"):
        return "Item Reported Successfully!"
    else:
        return "Item Report Failed. Please Try Again."

def RemoveItem(id, item_collection = items_collection,
                flagged_item_collection = flagged_items_collection):
    """
    This removes an item (if eligible)
    """
    # ADD IF STATEMENT THAT DOES NOT ALLOW ITEM TO BE
    # REMOVED IF THERE ARE ALREADY BIDS ON IT....
    # NEEDS TO CALL THE AUCTIONS MICROSERVICE
    if (False): # call to microservice
        return """There are already bids on 
                this item! It cannot be deleted"""

    find_item = {"_id": id}
    item_collection.delete_one(find_item)

    find_flags = {"itemID": id}
    flagged_item_collection.delete_many(find_flags)

    if (len(list(item_collection.find(find_item))) == 0
        and len(list(flagged_item_collection.find(find_flags))) == 0):
        return "Item Successfully Deleted."
    else:
        return "Item Was Not Deleted! Please Try Again."

def AddUserToWatchlist(id, user_id, collection = items_collection):
    """
    This adds a user to the watchlist
    """
    query = { "_id": id }
    modification = { "$addToSet": {"watchlist" : user_id }}
    result = collection.update_one(query, modification)

    if len(list(collection.find(query))) == 0:
        return "Item was not in the database."
    if result.modified_count > 0:
        return "Successfully added user to Watchlist."
    elif user_id in set(list(collection.find(query))[0]["watchlist"]):
        return "User was already in Watchlist."
    else:
        return "Addition Failed. Please try again."


def searchItem(keywords, collection = items_collection):
    """
    This searches the items in the database
    
    input:
    keywords (array of strings)
    """
    query = { "$or": []}
    for word in keywords:
        query["$or"].append({ "name" : {'$regex': word}})
        query["$or"].append({ "description" : {'$regex': word}})
    
    results = list(collection.find(query))
    return results

# executing tests for my functions
if __name__ == '__main__':
    
    print("Search Item Test: ")
    print(searchItem(["may", "agreeable"]))
    
    print("Add User To Watchlist Test: ")
    print(AddUserToWatchlist("a7ccc7e1-aaf", "30eeebf4-e79"))

    print("Remove Item From Items List Test: ")
    print(RemoveItem("a7ccc7e1-aaf"))

    print("Report Item Test/ Add Flagged Item Test: ")
    print(ReportItem("5b72cf57-5af", "counterfeit"))

    print("Get Item Test: ")
    print(GetItem("5b72cf57-5af"))

    print("Modify Item Test: ")
    print(ModifyItem("5b72cf57-5af", "lemon bars"))

    print("Add Items: ")
    print(AddItem("a7ccc7e1-aaf", "potato test",
            "re you do by for and not almost of  I to  an dark but not ran",
            ["Jewelry", "Watches"], "0aa271bf-1b4", "492674a4-bbe",
            23.82, False, ['e987d79c-4e8', '371ce498-44a', '4c16a517-749']))

    print("Edit Categories Test: ")
    print(EditCategories("a7ccc7e1-aaf", ["potato"]))

    print("View Flagged Items Test: ")
    print(ViewFlaggedItems())
    
    """
    This is the command to run to create the database in mongo db
    create_all_databases("../../data/mock_data/items.csv", 
                        "../../data/mock_data/flagged_items.csv",
                        "../../data/mock_data/photos.csv")
    """




    

    