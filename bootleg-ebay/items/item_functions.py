import csv
import json
import os
import re
import socket
import uuid
import items

from pymongo import MongoClient
from bson.objectid import ObjectId

class APIError(Exception):
    """All custom API Exceptions"""
    pass 

class BadInputError(APIError):
    """Custom bad input error class."""
    code = 400
    description = "Bad input Error"

class ItemsDBManager:

    @classmethod
    def _create_client(cls):
        hostname = os.getenv('ITEMSDBHOST', "localhost")
        client = MongoClient("mongodb://root:bootleg@" + hostname + ":27017")
        return client

    
    @classmethod
    def view_all_items(cls, limit = None):
        """
        This returns back all available items
        in sorted order
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]
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
        with cls._create_client() as client:
            collections = client["items"] 

            items_collection, flagged_items_collection = collections['items'], collections["flagged_items"]
            query = {"isFlagged": "True"}

            results = list(items_collection.find(query))
            to_return = []
            for result in results:
                new_item = result
                item_id = result[0]
                query = {"itemID": item_id}
                flagged = list(flagged_items_collection.find(query))
                reasons = []
                for flag in flagged:
                    reasons.append(flagged["FlagReason"])
                new_item["FlagReason"] = reasons
                to_return.append(new_item)
            if limit:

                return to_return[:limit]
            else:
                return to_return
    
    @classmethod
    def get_all_items(cls):
        """
        This gets all the items from the items collection
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]
            items = list(items_collection.find({}))
            return items
    
    @classmethod
    def get_item(cls, id):
        """
        this gets an item from the items collection
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]
            query = {"_id": id}
            results = list(items_collection.find(query))
            return results

    @classmethod
    def edit_categories(cls, item_id, updated_categories):
        """
        This edits the categories for an item
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]

            query = {"_id": item_id}
            new_categories = { "$set": { "category": updated_categories } }
            result = items_collection.update_one(query, new_categories)
            if result.modified_count > 0:
                return "Change was Successful!"
            else:
                raise BadInputError("Change was not Successful. Please Try Again.")
    
    @classmethod
    def add_item(cls, name, description, category, photos, 
                sellerID, quantity):
        """
        This adds an item to the items collection
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]
            photos_collection = collections["photos"]

            # first upload photo to photos_collection
            photo_id = ObjectId()
            new_photo = {"_id": photo_id, "photo": photos}
            result = photos_collection.insert_one(new_photo)


            item = {"name": None, "description": None,
                    "category": None, "photos": None, "sellerID": None,
                    "isFlagged": False, "watchlist": None, "quantity": None}
            item["_id"] = ObjectId()
            item["name"] = name
            item["description"] = description
            item["category"] = category
            item["photos"] = photo_id
            item["sellerID"] = sellerID
            item["watchlist"] = []
            item["quantity"] = quantity
            result = items_collection.insert_one(item)

            if len(list(items_collection.find({ "_id": item["_id"]}))) == 1:
                item = list(items_collection.find({ "_id": item["_id"]}))
                item[0]["_id"] = str(item[0]["_id"])
                item[0]["photos"] = photos
                return item[0]
            else:
                raise BadInputError("Item was not successfully inserted. Please Try Again.")

    @classmethod
    def modify_item(cls, id, name = None, description = None,
                category = None, photos = None,
                watchlist = None, quantity = None):
        """
        With this function, I can modify the item
        that matches the given id.
        I can modify the name, description, category,
        photos, and price
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]

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
        with cls._create_client() as client:
            collections = client["items"] 
            flagged_items_collection = collections["flagged_items"]

            all_items = []
            for item in items:
                id = item["_id"]
                name = item["name"]
                description = item["description"]
                category = item["category"]
                photos = item["photos"]
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
                            sellerID, isFlagged, FlaggedReason,
                            watchlist, quantity, id))
            return all_items


    @classmethod
    def add_flagged_item(cls, item_id, flag_reason):
        """
        This adds a new flag to the database
        """
        with cls._create_client() as client:
            collections = client["items"] 
            flagged_items_collection = collections["flagged_items"]

            item = {"itemID": item_id, "FlagReason": flag_reason}
            inserted_item = flagged_items_collection.insert_one(item)


            if len(list(flagged_items_collection.find({"itemID" : item_id, "FlagReason": flag_reason}))) > 0:
                return "Flag Successfully Added!"
            else:
                raise BadInputError("Flag Failure. Please Try Again.")


    @classmethod
    def report_item(cls, id, flag_reason):
        """
        This flags an item, and gives the flag reason
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]

            # updates item database
            query = {"_id": id}
            flag = {"$set" : {"isFlagged" : "True" }}
            update_result = items_collection.update_one(query, flag)

            
            # updates flagged items database
            result = cls.add_flagged_item(id, flag_reason)
            if (result == "Flag Successfully Added!"):
                return "Item Reported Successfully!"
            else:
                raise BadInputError("Item Report Failed. Please Try Again.")

    @classmethod
    def remove_item(cls, id):
        """
        This removes an item
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]
            flagged_items_collection = collections["flagged_items"]
            find_item = {"_id": id}
            items_collection.delete_one(find_item)

            find_flags = {"itemID": id}
            flagged_items_collection.delete_many(find_flags)

            if (len(list(items_collection.find(find_item))) == 0
                and len(list(flagged_items_collection.find(find_flags))) == 0):
                return "Item Successfully Deleted."
            else:
                raise BadInputError("Item Was Not Deleted! Please Try Again.")

    @classmethod
    def add_user_to_watch_list(cls, id, watchlist_item):
        """
        This adds a user to the watchlist
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]

            query = { "_id": id }
            modification = { "$addToSet": {"watchlist" : watchlist_item }}
            result = items_collection.update_one(query, modification)

            if len(list(items_collection.find(query))) == 0:
                raise BadInputError("Item was not in the database.")
            if result.modified_count > 0:
                return "Successfully added user to Watchlist."
            else:
                raise BadInputError("Addition Failed, or User was already in Watchlist. Please try again.")

    @classmethod
    def search_item(cls, keywords, category):
        """
        This searches the items in the database
        
        input:
        keywords (array of strings)
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]


            if keywords and category:
                main_query = {"$and": []}
                query = { "$or": []}
                for word in keywords:
                    query["$or"].append({ "name" : {'$regex': word}})
                    query["$or"].append({ "description" : {'$regex': word}})

                main_query["$and"].append(query)
                query = {"category": { '$in' : category }}
                main_query["$and"].append(query)
                results = list(items.collection.find(main_query))
                return results

            if keywords:
                query = { "$or": []}
                for word in keywords:
                    query["$or"].append({ "name" : {'$regex': word}})
                    query["$or"].append({ "description" : {'$regex': word}})
                keyword_results = list(items.collection.find(query))
                return keyword_results

            if category:
                query = {"category": { '$in' : category }}
                category_results = list(items_collection.find(query))
                return category_results

    @classmethod
    def modify_quantity(cls, item_id):
        """
        This adjusts the quantity of the item. If
        the quantity was successfully changed, it indicates it.
        """
        with cls._create_client() as client:
            collections = client["items"] 
            items_collection = collections["items"]
            query = {"_id" : item_id}
            item = list(items_collection.find(query))
            quantity = item[0]["quantity"]
            if quantity < 1:
                raise BadInputError("Was unable to adjust quantity. Item is sold out.")
            modification = { "$set": {"quantity" : quantity - 1 }}
            result = items_collection.update_one(query, modification)
            if result.modified_count > 0:
                return "Successfully adjusted quantity."
            else:
                raise BadInputError("Was unable to adjust quantity. Item is sold out.")

    @classmethod
    def get_flag_reasons(cls, item_id):
        """
        This returns back the flagged reasons for a particular id.
        """
        with cls._create_client() as client:
            collections = client["items"] 
            flagged_items_collection = collections["flagged_items"]
            query = {"itemID" : item_id}
            result = list(flagged_items_collection.find(query))
            return result
    
    @classmethod
    def get_photo(cls, photo_id):
        """
        This returns back the photo with the specified id
        """
        with cls._create_client() as client:
            collections = client["items"] 
            photos_collection = collections["photos"]
            photo_id = ObjectId(photo_id)
            query = {'_id': photo_id}
            result = list(photos_collection.find(query))
            if len(result) > 0:
                return result[0]["photo"]
            else:
                return None

    @classmethod
    def get_categories(cls):
        """
        This returns back all the categories
        """
        with cls._create_client() as client:
            collections = client["items"] 
            categories_collection = collections["categories"]

            result = list(categories_collection.find({}))
            return result[0]["categories"]
    
    @classmethod
    def add_category(cls, category):
        """
        This adds a category to the existing list of categories
        """
        with cls._create_client() as client:
            collections = client["items"] 
            categories_collection = collections["categories"]
            result = list(categories_collection.find({}))
            query = {'_id': result[0]["_id"]}
            modification = { "$addToSet": {"categories" : category }}
            result = categories_collection.update_one(query, modification)
            if result.modified_count > 0:
                return "Successfully added category!"
            else:
                raise BadInputError("Was unable to add category. The category either exists, or you should try again later.")
    
    @classmethod
    def remove_category(cls, category):
        with cls._create_client() as client:
            collections = client["items"] 
            categories_collection = collections["categories"]
            result = list(categories_collection.find({}))
            query = {'_id': result[0]["_id"]}
            current_categories = result[0]["categories"]
            current_categories.remove(category)

            modification = { "$set": {"categories" : current_categories }}

            result = categories_collection.update_one(query, modification)
            if result.modified_count > 0:
                return "Successfully removed category!"
            else:
                raise BadInputError("Was unable to remove category. The category either exists, or you should try again later.")      




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
        if new_item.isFlagged == "True":
            new_dict = new_item.to_mongo()
            new_item.Flagged_Reason
            new_dict["_id"] = str(item_id)
            new_dict["flagged_reasons"] = new_item.Flagged_Reason
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


def search_item(keywords, category):
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
        if new_item.matches_search(keywords, category):
            new_dict = new_item.to_mongo()
            new_dict["_id"] = str(item_id)
            item_objects.append(new_dict)
    return json.dumps(item_objects)

def add_user_to_watch_list(item_id, watchlist_item):
    """
    This adds a user to the watchlist
    """
    item_id = ObjectId(item_id)
    item = ItemsDBManager.get_item(item_id)[0]
    flags = ItemsDBManager.get_flag_reasons(item_id)
    photo = ItemsDBManager.get_photo(item["photos"])
        
    new_item = items.Item()
    new_item.from_mongo(item, flags, photo)
    new_item.add_user_to_watchlist(watchlist_item)
    return json.dumps(ItemsDBManager.modify_item(new_item.id, None, None, None,
                                    None, new_item.watchlist, None))

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
    flags = ItemsDBManager.get_flag_reasons(item_id)
    new_item["flagged_reasons"] = []
    for flag in flags:
        new_item["flagged_reasons"].append(flag["FlagReason"])
    photo = ItemsDBManager.get_photo(new_item["photos"])
    new_item["photos"] = photo
    new_item["_id"] = str(item_id)
    return json.dumps(new_item)

def modify_item(item_id, name = None, description = None,
                category = None, photos = None, 
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
                        category, watchlist, quantity)

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
    if watchlist:
        new_watchlist = new_item.watchlist
    else:
        new_watchlist = None
    if quantity:
        new_quantity = new_item.quantity
    else:
        new_quantity = None

    return json.dumps(ItemsDBManager.modify_item(item_id, new_name, new_description,
                                        new_category, new_photos,
                                        new_watchlist, new_quantity))

def add_item(name, description, category, 
                photos, sellerID, quantity):
    """
    This adds the item
    """
    new_item = items.Item(name, description, category,
                            photos, sellerID, False,
                            None, None, quantity, None)
    return json.dumps(ItemsDBManager.add_item(new_item.name, new_item.description,
                            new_item.category, new_item.photos,
                            new_item.sellerID, new_item.quantity))

def edit_categories(item_id, new_categories):
    item_id = ObjectId(item_id)
    item = ItemsDBManager.get_item(item_id)[0]
    flags = ItemsDBManager.get_flag_reasons(item_id)
    photo = ItemsDBManager.get_photo(item["photos"])
    new_item = items.Item()
    new_item.from_mongo(item, flags, photo)

    new_item.edit_categories(new_categories)
    return json.dumps(ItemsDBManager.modify_item(new_item.id, None, None, new_item.category,
                                None, None))

def modify_quantity(item_id):
    item_id = ObjectId(item_id)
    item = ItemsDBManager.get_item(item_id)[0]
    flags = ItemsDBManager.get_flag_reasons(item_id)
    photo = ItemsDBManager.get_photo(item["photos"])
    new_item = items.Item()

    new_item.from_mongo(item, flags, photo)
    new_item.modify_item(None, None, None, None,
                        None, new_item.quantity - 1)
    return json.dumps(ItemsDBManager.modify_quantity(new_item.id))

def get_categories():
    return json.dumps(ItemsDBManager.get_categories())

def add_categories(category):
    return json.dumps(ItemsDBManager.add_category(category))

def remove_categories(category):
    return json.dumps(ItemsDBManager.remove_category(category))

def items_by_seller(seller_id):
    all_items = ItemsDBManager.get_all_items()
    item_objects = []
    for item in all_items:
        item_id = item["_id"]
        flags = ItemsDBManager.get_flag_reasons(item_id)
        photo = ItemsDBManager.get_photo(item["photos"])
        
        new_item = items.Item()
        new_item.from_mongo(item, flags, photo)

        if new_item.sellerID == int(seller_id):
            new_dict = new_item.to_mongo()
            new_dict["_id"] = str(item_id)
            item_objects.append(new_dict)
    return json.dumps(item_objects)




# executing tests for my functions
if __name__ == '__main__':
    #print(items_by_seller("27"))
    #print(view_all_items())
    """
    print(add_categories("Food"))
    print(remove_categories("Food"))
    """
    print("Search Item Test: ")
    print(search_item(None, "Watches"))
    

    #print("Add Items: ")
    #print(add_item("potato test",
    #        "test",
    #        ["Jewelry", "Watches"], 
    #        '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', "for_see_room",
    #        6))
    #view_flagged_items()
    """
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