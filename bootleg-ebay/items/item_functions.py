import csv
import json
import os
import re
import socket
import uuid
import items

from pymongo import MongoClient
from bson.objectid import ObjectId



class ItemsDBManager:
    @classmethod
    def _init_items_collection(cls):
        hostname = os.getenv('ITEMSDBHOST', "localhost")
        client = MongoClient("mongodb://root:bootleg@" + hostname + ":27017")
        db = client["items"]
        items_collection = db["items"]
        flagged_items_collection = db["flagged_items"]
        photos_collection = db["photos"]
        return items_collection, flagged_items_collection, photos_collection
    
    @classmethod
    def view_all_items(cls, limit = None):
        """
        This returns back all available items
        in sorted order
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"quantity" : {"$gte": 0}}
        results = list(items_collection.find(query))
        if limit:
            return results[:limit]
        else:
            return results

    @classmethod
    def view_flagged_items(cls, limit = None):
        """
        This returns all the flagged items
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"isFlagged": "True"}

        results = list(items_collection.find(query))
        if limit:
            return results[:limit]
        else:
            return results
    
    @classmethod
    def get_all_items(cls):
        """
        This gets all the items from the items collection
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        items = list(items_collection.find({}))
        return items
    
    @classmethod
    def get_item(cls, id):
        """
        this gets an item from the items collection
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"_id": id}
        results = list(items_collection.find(query))
        return results

    @classmethod
    def edit_categories(cls, item_id, updated_categories):
        """
        This edits the categories for an item
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"_id": item_id}
        new_categories = { "$set": { "category": updated_categories } }
        result = items_collection.update_one(query, new_categories)
        if result.modified_count > 0:
            return "Change was Successful!"
        else:
            return "Change was not Successful. Please Try Again."
    
    @classmethod
    def add_item(cls, name, description, category, photos, 
                sellerID, price, quantity):
        """
        This adds an item to the items collection
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        item = {"name": None, "description": None,
                "category": None, "photos": None, "sellerID": None,
                "price": None, "isFlagged": False, "watchlist": None, "quantity": None}
        item["_id"] = ObjectId()
        item["name"] = name
        item["description"] = description
        item["category"] = category
        item["photos"] = photos
        item["sellerID"] = sellerID
        item["price"] = price
        item["watchlist"] = []
        item["quantity"] = quantity
        result = items_collection.insert_one(item)

        if len(list(items_collection.find({ "_id": item["_id"]}))) == 1:
            return "Item Successfully Inserted!"
        else:
            return "Item was not successfully inserted. Please Try Again."

    @classmethod
    def modify_item(cls, id, name = None, description = None,
                category = None, photos = None, price = None,
                watchlist = None, quantity = None):
        """
        With this function, I can modify the item
        that matches the given id.

        I can modify the name, description, category,
        photos, and price
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()

        query = {"_id": id}
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
        if watchlist:
            new_watchlist = { "$set": { "watchlist": watchlist } }
            modifications.append(new_watchlist)
        if quantity:
            new_quantity = {"$set": {"quantity": quantity}}
            modifications.append(new_quantity)
        success = []
        failure = []
        for modification in modifications:
            result = items_collection.update_one(query, modification)
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

    @classmethod
    def convert_to_item_objects(cls, items):
        """
        This gets all the documents from the items database,
        and uploads them into objects of the items class
        and returns back an array of these items.
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        all_items = []
        for item in items:
            id = item["_id"]
            name = item["name"]
            description = item["description"]
            category = item["category"]
            photos = item["photos"]
            price = item["price"]
            sellerID = item["sellerID"]
            isFlagged = item["isFlagged"]
            FlaggedReason = []
            if isFlagged == True:
                query = {"itemID" : id}
                results = list(flagged_items_collection.find(query))
                for result in results:
                    FlaggedReason.append(result["FlagReason"])
                flags = {}
            watchlist = item["watchlist"]
            quantity = item["quantity"]
            all_items.append(items.Item(name, description, category, photos,
                        sellerID, price, isFlagged, FlaggedReason,
                        watchlist, quantity, id))
        return all_items


    @classmethod
    def add_flagged_item(cls, item_id, flag_reason):
        """
        This adds a new flag to the database
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        item = {"itemID": item_id, "FlagReason": flag_reason}
        inserted_item = flagged_items_collection.insert_one(item)


        if len(list(flagged_items_collection.find({"itemID" : item_id, "FlagReason": flag_reason}))) > 0:
            return "Flag Successfully Added!"
        else:
            return "Flag Failure. Please Try Again."


    @classmethod
    def report_item(cls, id, flag_reason):
        """
        This flags an item, and gives the flag reason
        """
        # updates item database
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"_id": id}
        flag = {"$set" : {"isFlagged" : "True" }}
        update_result = items_collection.update_one(query, flag)

        
        # updates flagged items database
        result = cls.add_flagged_item(id, flag_reason)
        if (result == "Flag Successfully Added!"):
            return "Item Reported Successfully!"
        else:
            return "Item Report Failed. Please Try Again."

    @classmethod
    def remove_item(cls, id):
        """
        This removes an item
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        find_item = {"_id": id}
        items_collection.delete_one(find_item)

        find_flags = {"itemID": id}
        flagged_items_collection.delete_many(find_flags)

        if (len(list(items_collection.find(find_item))) == 0
            and len(list(flagged_items_collection.find(find_flags))) == 0):
            return "Item Successfully Deleted."
        else:
            return "Item Was Not Deleted! Please Try Again."

    @classmethod
    def add_user_to_watch_list(cls, id, user_id):
        """
        This adds a user to the watchlist
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = { "_id": id }
        modification = { "$addToSet": {"watchlist" : user_id }}
        result = items_collection.update_one(query, modification)

        if len(list(items_collection.find(query))) == 0:
            return "Item was not in the database."
        if result.modified_count > 0:
            return "Successfully added user to Watchlist."
        elif user_id in set(list(items_collection.find(query))[0]["watchlist"]):
            return "User was already in Watchlist."
        else:
            return "Addition Failed. Please try again."

    @classmethod
    def search_item(cls, keywords):
        """
        This searches the items in the database
        
        input:
        keywords (array of strings)
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = { "$or": []}
        for word in keywords:
            query["$or"].append({ "name" : {'$regex': word}})
            query["$or"].append({ "description" : {'$regex': word}})
        
        results = list(items.collection.find(query))
        return results

    @classmethod
    def modify_quantity(cls, item_id):
        """
        This adjusts the quantity of the item. If
        the quantity was successfully changed, it indicates it.
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"_id" : item_id}
        item = list(items_collection.find(query))
        quantity = item[0]["quantity"]
        modification = { "$set": {"quantity" : quantity - 1 }}
        result = items_collection.update_one(query, modification)
        if result.modified_count > 0:
            return "Successfully adjusted quantity."
        else:
            return "Was unable to adjust quantity. Item is sold out."

    @classmethod
    def get_flag_reasons(cls, item_id):
        """
        This returns back the flagged reasons for a particular id.
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"_id" : item_id}
        result = list(flagged_items_collection.find(query))
        return result
    
    @classmethod
    def get_photo(cls, photo_id):
        """
        This returns back the photo with the specified id
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        photo_id = ObjectId(photo_id)
        query = {'_id': photo_id}
        result = list(photos_collection.find(query))
        if len(result) > 0:
            return result[0]["photo"]
        else:
            return None


def view_flagged_items(limit = None):
    """
    This function searches through all the items and returns
    the ones that are flagged
    """
    all_items = ItemsDBManager.get_all_items()
    item_objects = []
    for item in all_items:
        item_id = item["_id"]
        flags = ItemsDBManager.get_flag_reasons(item_id)
        photo = ItemsDBManager.get_photo(item["photos"])
        

        new_item = items.Item()
        new_item.from_mongo(item, flags, photo)
        if new_item.isFlagged:
            new_dict = new_item.to_mongo()
            new_dict["_id"] = str(item_id)
            item_objects.append(new_dict)
        if limit:
            if len(item_objects) == limit:
                break
    return json.dumps(item_objects)


def view_all_items(limit = None):
    """
    This returns back a list of all items
    """
    # The only available items are items
    # that are currently being auctioned

    all_items = ItemsDBManager.get_all_items()
    item_objects = []
    for item in all_items:
        item_id = item["_id"]
        flags = ItemsDBManager.get_flag_reasons(item_id)
        photo = ItemsDBManager.get_photo(item["photos"])

        new_item = items.Item()
        new_item.from_mongo(item, flags, photo)
        if new_item.quantity > 0:
            new_dict = new_item.to_mongo()
            new_dict["_id"] = str(item_id)
            item_objects.append(new_dict)
        if limit:
            if len(item_objects) == limit:
                break
    return json.dumps(item_objects)


def search_item(keywords):
    """
    This function searches through all the items and returns
    the ones that match the search criteria
    """
    all_items = ItemsDBManager.get_all_items()
    item_objects = []
    for item in all_items:
        item_id = item["_id"]
        flags = ItemsDBManager.get_flag_reasons(item_id)
        photo = ItemsDBManager.get_photo(item["photos"])
        
        new_item = items.Item()
        new_item.from_mongo(item, flags, photo)
        if new_item.matches_search(keywords):
            item_objects.append(new_item.to_mongo())
    return json.dumps(item_objects)

def add_user_to_watch_list(item_id, user_id):
    """
    This adds a user to the watchlist
    """
    item_id = ObjectId(item_id)
    item = ItemsDBManager.get_item(item_id)[0]
    flags = ItemsDBManager.get_flag_reasons(item_id)
    photo = ItemsDBManager.get_photo(item["photos"])
        
    new_item = items.Item()
    new_item.from_mongo(item, flags, photo)
    new_item.add_user_to_watchlist(user_id)
    return json.dumps(ItemsDBManager.modify_item(new_item.id, None, None, None, None,
                                    None, new_item.watchlist))

def remove_item(item_id):
    """
    This removes an item from the database
    """
    item_id = ObjectId(item_id)
    return json.dumps(ItemsDBManager.remove_item(item_id))

def report_item(item_id, reason):
    """
    This reports an item
    """
    item_id = ObjectId(item_id)
    item = ItemsDBManager.get_item(item_id)[0]
    flags = ItemsDBManager.get_flag_reasons(item_id)
    photo = ItemsDBManager.get_photo(item["photos"])
        
    new_item = items.Item()
    new_item.from_mongo(item, flags, photo)
    new_item.report_item(reason)
    return json.dumps(ItemsDBManager.report_item(new_item.id, reason))

def get_item(item_id):
    """
    This gets an item from the database
    """
    item_id = ObjectId(item_id)
    new_item = ItemsDBManager.get_item(item_id)[0]
    photo = ItemsDBManager.get_photo(new_item["photos"])
    new_item["photos"] = photo
    new_item["_id"] = str(item_id)
    return json.dumps(new_item)

def modify_item(item_id, name = None, description = None,
                category = None, photos = None, price = None,
                watchlist = None, quantity = None):
    """
    This modifies the item
    """
    item_id = ObjectId(item_id)
    item = ItemsDBManager.get_item(item_id)[0]
    flags = ItemsDBManager.get_flag_reasons(item_id)
    photo = ItemsDBManager.get_photo(item["photos"])
    new_item = items.Item()
    new_item.from_mongo(item, flags, photo)
    new_item.modify_item(name, description, photos,
                        price, category, watchlist, quantity)

    if name:
        new_name = new_item.name
    else:
        new_name = None
    if description:
        new_description = new_item.description
    else:
        new_description = None
    if category:
        new_category = new_item.category
    else:
        new_category = None
    if photos:
        new_photos = new_item.photos
    else:
        new_photos = None
    if price:
        new_price = new_item.price
    else:
        new_price = None
    if watchlist:
        new_watchlist = new_item.watchlist
    else:
        new_watchlist = None
    if quantity:
        new_quantity = new_item.quantity
    else:
        new_quantity = None
    return json.dumps(ItemsDBManager.modify_item(item_id, new_name, new_description,
                                        new_category, new_photos, new_price, 
                                        new_watchlist, new_quantity))

def add_item(name, description, category, 
                photos, sellerID, price, quantity):
    """
    This adds the item
    """
    new_item = items.Item(name, description, category,
                            photos, sellerID, price, False,
                            None, None, quantity, None)
    return json.dumps(ItemsDBManager.add_item(new_item.name, new_item.description,
                            new_item.category, new_item.photos,
                            new_item.sellerID, new_item.price, new_item.quantity))

def edit_categories(item_id, new_categories):
    item_id = ObjectId(item_id)
    item = ItemsDBManager.get_item(item_id)[0]
    flags = ItemsDBManager.get_flag_reasons(item_id)
    photo = ItemsDBManager.get_photo(item["photos"])
    new_item = items.Item()
    new_item.from_mongo(item, flags, photo)

    new_item.edit_categories(new_categories)
    return json.dumps(ItemsDBManager.modify_item(new_item.id, None, None, new_item.category,
                                None, None, None))

def modify_quantity(item_id):
    item_id = ObjectId(item_id)
    item = ItemsDBManager.get_item(item_id)[0]
    flags = ItemsDBManager.get_flag_reasons(item_id)
    photo = ItemsDBManager.get_photo(item["photos"])
    new_item = items.Item()

    new_item.from_mongo(item, flags, photo)
    new_item.modify_item(None, None, None, None,
                        None, None, new_item.quantity - 1)
    return json.dumps(ItemsDBManager.modify_quantity(new_item.id))



# executing tests for my functions
if __name__ == '__main__':
    pass
    """
    print("Search Item Test: ")
    print(search_item(["and"]))

    print("Add Items: ")
    print(add_item("potato test",
            "test",
            ["Jewelry", "Watches"], "618ac0a5c43212f2d81be436", "for_see_room",
            23.82, 6))
    

    print("Add User To Watchlist Test: ")
    print(add_user_to_watch_list("618af8fde27c0181a0bc9bac", "example_user"))

    

    
    print("Report Item Test/ Add Flagged Item Test: ")
    print(report_item("618af8fde27c0181a0bc9bac", "counterfeit"))
    
    
    print("Get Item Test: ")
    print(get_item("618af8fde27c0181a0bc9bac"))

    
    print("Modify Item Test: ")
    print(modify_item("618af8fde27c0181a0bc9bac", "lemon bars"))

    
    print("Edit Categories Test: ")
    print(edit_categories("618af8fde27c0181a0bc9bac", ["potato"]))
    
    print("View Flagged Items Test: ")
    print(view_flagged_items())
    
    
    print("Modify Quantity Test: ")
    print(modify_quantity("618af8fde27c0181a0bc9bac"))
    
    
    print("Remove Item From Items List Test: ")
    print(remove_item("618af8fde27c0181a0bc9bac"))
    """
    