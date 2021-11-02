import csv
import json
import os
import re
import socket
import uuid
import items

from pymongo import MongoClient



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
    def ViewFlaggedItems(cls, limit = None):
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
    def GetAllItems(cls):
        """
        This gets all the items from the items collection
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        items = list(items_collection.find({}))
        return items
    
    @classmethod
    def GetItem(cls, id):
        """
        this gets an item from the items collection
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"_id": id}
        results = list(items_collection.find(query))
        return results

    @classmethod
    def EditCategories(cls, item_id, updated_categories):
        """
        This edits the categories for an item
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = { "_id" : item_id }
        new_categories = { "$set": { "category": updated_categories } }
        result = items_collection.update_one(query, new_categories)
        if result.modified_count > 0:
            return "Change was Successful!"
        else:
            return "Change was not Successful. Please Try Again."
    
    @classmethod
    def AddItem(cls, name, description, category, photos, 
                sellerID, price):
        """
        This adds an item to the items collection
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        item = {"name": None, "description": None,
                "category": None, "photos": None, "sellerID": None,
                "price": None, "isFlagged": False, "watchlist": None, "available": None}
        item["name"] = name
        item["description"] = description
        item["category"] = category
        item["photos"] = photos
        item["sellerID"] = sellerID
        item["price"] = price
        item["watchlist"] = []
        item["available"] = True
        result = items_collection.insert_one(item)

        if len(list(items_collection.find({ "_id": item["_id"]}))) == 1:
            return "Item Successfully Inserted!"
        else:
            return "Item was not successfully inserted. Please Try Again."

    @classmethod
    def ModifyItem(cls, id, name = None, description = None,
                category = None, photos = None, price = None,
                watchlist = None):
        """
        With this function, I can modify the item
        that matches the given id.

        I can modify the name, description, category,
        photos, and price
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()

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
        if watchlist:
            new_watchlist = { "$set": { "watchlist": watchlist } }
            modifications.append(new_watchlist)

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
    def ConvertToItemObjects(cls, items):
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
            available = item["available"]
            all_items.append(items.Item(name, description, category, photos,
                        sellerID, price, isFlagged, FlaggedReason,
                        watchlist, available, id))
        return all_items


    @classmethod
    def AddFlaggedItem(cls, item_id, flag_reason):
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
    def ReportItem(cls, id, flag_reason):
        """
        This flags an item, and gives the flag reason
        """
        # updates item database
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"_id": id}
        flag = {"$set" : {"isFlagged" : "True" }}
        update_result = items_collection.update_one(query, flag)

        
        # updates flagged items database
        result = cls.AddFlaggedItem(id, flag_reason)
        if (result == "Flag Successfully Added!"):
            return "Item Reported Successfully!"
        else:
            return "Item Report Failed. Please Try Again."

    @classmethod
    def RemoveItem(cls, id):
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
    def AddUserToWatchlist(cls, id, user_id):
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
    def searchItem(cls, keywords):
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
    def modifyAvailability(cls, item_id):
        """
        This adjusts the availability of the item. If
        the availability was successfully changed, it indicates it.
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"_id" : item_id}
        modification = { "$set": {"available" : False }}
        result = items_collection.update_one(query, modification)
        if result.modified_count > 0:
            return "Successfully adjusted availability."
        else:
            return "Was unable to adjust availability. Item is no longer available."

    @classmethod
    def getFlagReasons(cls, item_id):
        """
        This returns back the flagged reasons for a particular id.
        """
        items_collection, flagged_items_collection, photos_collection = cls._init_items_collection()
        query = {"_id" : item_id}
        result = list(flagged_items_collection.find(query))
        return result


def ViewFlaggedItems(limit = None):
    """
    This function searches through all the items and returns
    the ones that are flagged
    """
    all_items = ItemsDBManager.GetAllItems()
    item_objects = []
    for item in all_items:
        item_id = item["_id"]
        flags = ItemsDBManager.getFlagReasons(item_id)
        new_item = items.Item()
        new_item.from_mongo(item, flags)
        if new_item.isFlagged:
            new_dict = new_item.to_mongo()
            item_objects.append(new_dict)
        if limit:
            if len(item_objects) == limit:
                break
    return json.dumps(item_objects)


def SearchItem(keywords):
    """
    This function searches through all the items and returns
    the ones that match the search criteria
    """
    all_items = ItemsDBManager.GetAllItems()
    item_objects = []
    for item in all_items:
        item_id = item["_id"]
        flags = ItemsDBManager.getFlagReasons(item_id)
        new_item = items.Item()
        new_item.from_mongo(item, flags)
        if new_item.matches_search(keywords):
            item_objects.append(new_item.to_mongo())
    return json.dumps(item_objects)

def AddUserToWatchlist(item_id, user_id):
    """
    This adds a user to the watchlist
    """
    item = ItemsDBManager.GetItem(item_id)[0]
    flags = ItemsDBManager.getFlagReasons(item_id)
    new_item = items.Item()
    new_item.from_mongo(item, flags)
    new_item.addUserToWatchlist(user_id)
    return json.dumps(ItemsDBManager.ModifyItem(new_item.id, None, None, None, None,
                                    None, new_item.watchlist))

def RemoveItem(item_id):
    """
    This removes an item from the database
    """
    return json.dumps(ItemsDBManager.RemoveItem(item_id))

def ReportItem(item_id, reason):
    """
    This reports an item
    """
    item = ItemsDBManager.GetItem(item_id)[0]
    flags = ItemsDBManager.getFlagReasons(item_id)
    new_item = items.Item()
    new_item.from_mongo(item, flags)
    new_item.report_item(reason)
    return json.dumps(ItemsDBManager.ReportItem(new_item.id, reason))

def GetItem(item_id):
    """
    This gets an item from the database
    """
    return json.dumps(ItemsDBManager.GetItem(item_id)[0])

def ModifyItem(item_id, name = None, description = None,
                category = None, photos = None, price = None,
                watchlist = None):
    """
    This modifies the item
    """
    item = ItemsDBManager.GetItem(item_id)[0]
    flags = ItemsDBManager.getFlagReasons(item_id)
    new_item = items.Item()
    new_item.from_mongo(item, flags)
    new_item.modifyItem(name, description, category, photos,
                        price, watchlist)
    if name:
        new_name = new_item.name
    else:
        name = None
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
    
    return json.dumps(ItemsDBManager.ModifyItem(item_id, new_name, new_description,
                                        new_category, new_photos, new_price, 
                                        new_watchlist))

def AddItem(name, description, category, 
                photos, sellerID, price):
    """
    This adds the item
    """
    new_item = items.Item(name, description, category,
                            photos, sellerID, price, False,
                            None, None, True, None)
    return json.dumps(ItemsDBManager.AddItem(new_item.name, new_item.description,
                            new_item.category, new_item.photos,
                            new_item.sellerID, new_item.price))

def EditCategories(item_id, new_categories):
    item = ItemsDBManager.GetItem(item_id)[0]
    flags = ItemsDBManager.getFlagReasons(item_id)
    new_item = items.Item()
    new_item.from_mongo(item, flags)

    new_item.editCategories(new_categories)
    return json.dumps(ItemsDBManager.ModifyItem(new_item.id, None, None, new_item.category,
                                None, None, None))

def ModifyAvailability(item_id):
    item = ItemsDBManager.GetItem(item_id)[0]
    flags = ItemsDBManager.getFlagReasons(item_id)
    new_item = items.Item()
    new_item.from_mongo(item, flags)
    new_item.modifyItem(None, None, None, None,
                        None, None, False)
    return json.dumps(ItemsDBManager.modifyAvailability(new_item.id))



# executing tests for my functions
if __name__ == '__main__':
    
    print("Search Item Test: ")
    print(SearchItem(["caught"]))
    
    print("Add User To Watchlist Test: ")
    print(AddUserToWatchlist("7ed25c8c-89b", "d35d484e-d66"))

    print("Remove Item From Items List Test: ")
    print(RemoveItem("4e889ad4-74b"))

    print("Report Item Test/ Add Flagged Item Test: ")
    print(ReportItem("e176a0d8-1a2", "counterfeit"))

    print("Get Item Test: ")
    print(GetItem("0ff1cb38-5d1"))

    print("Modify Item Test: ")
    print(ModifyItem("0ff1cb38-5d1", "lemon bars"))

    print("Add Items: ")
    print(AddItem("potato test",
            "re you do by for and not almost of  I to  an dark but not ran",
            ["Jewelry", "Watches"], "0aa271bf-1b4", "492674a4-bbe",
            23.82))

    print("Edit Categories Test: ")
    print(EditCategories("0ff1cb38-5d1", ["potato"]))

    print("View Flagged Items Test: ")
    print(ViewFlaggedItems())

    print("Modify Availability Test: ")
    print(ModifyAvailability("0ff1cb38-5d1"))
    
