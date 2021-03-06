import random
import string
import datetime
import csv
from nltk.corpus import gutenberg
import re
import uuid
from PIL import Image
import io
from bson.objectid import ObjectId
import time
import base64



import os
import json
import random
import imghdr
import sys
import urllib.request
import urllib.parse

csv.field_size_limit(sys.maxsize)

def convert_image_to_string(image_directory):
    image = Image.open(image_directory)
    output = io.BytesIO()
    image.save(output, format="png")
    image_as_string = output.getvalue()
    return image_as_string



def generate_random_date(start_date, end_date):
    """
    returns a random date between a start date
    and an end date in epoch time
    """
    time_between_dates = (end_date - start_date).total_seconds()
    random_number_of_seconds = random.randrange(time_between_dates)
    random_date = start_date + datetime.timedelta(seconds = random_number_of_seconds)
    random_date_epoch_time = random_date.strftime('%s')
    return random_date_epoch_time

def generate_random_id():
    return ObjectId()

def generate_random_bool():
    random_bit = random.getrandbits(1)
    random_boolean = bool(random_bit)
    return random_boolean


def clean_data(words):
    """
    This cleans the list of words.
    """
    new_words = []
    for word in words:    
        new_words.append(re.sub(r'[^a-zA-Z0-9]', "", word))
    return new_words

def get_random_words(num_words, joiner):
    """
    This generates a random sequence of words
    """
    # I just want to get a corpus of words
    emma = gutenberg.words("austen-emma.txt")
    emma = clean_data(emma)

    return  joiner.join(random.choice(emma) for i in range(0, num_words))

def get_random_categories(num_categories):
    categories = ["Auto Parts and Accessories", "Automotive Tools & Supplies",
                    "Other Vehicles and Trailers", "Motorcycles",
                    "Powersport Vehicles", "Boats", "Top Vehicle Makes",
                    "Fashion", "Women's Clothing", "Women's Shoes",
                    "Women's Accessories", "Women's Bags & Handbangs",
                    "Men's Clothing", "Men's Shoes", "Men's Accessories",
                    "Kid's Clothing, Shoes, & Accessories", 
                    "Baby Clothing, Shoes, & Accessories", "Jewelry",
                    "Watches, Parts & Accessories"]
    selected_categories = []
    for i in range(0, num_categories):
        selected_categories.append(random.choice(categories))
    return selected_categories
    

def items():
    """
    Creates 30 items of data for the items database

    Schema: id, name, description,
            category, photos, sellerID,
            price, isFlagged
    """
    # getting names of potential sellers
    
    file = open("users.csv")
    csvreader = csv.reader(file)
    all_users = []
    for row in csvreader:
        all_users.append(row[0])
    file.close()

    all_photos = []
    file = open("photos.csv")
    csvreader = csv.reader(file)
    for row in csvreader:
        all_photos.append(row[0])
    file.close()

    all_items = []
    for i in range(0, 30):
        id = generate_random_id()
        name = get_random_words(3, " ")
        description = get_random_words(30, " ")
        categories = get_random_categories(3)
        photos = all_photos[i]
        seller_id = random.choice(list(range(1, 31)))
        
        isFlagged = False
        watch_list = []
        while len(watch_list) != 3:
            new = random.choice(list(range(1, 31)))
            if new not in watch_list:
                watch_list.append(new)
        quantity = random.choice(range(1, 11))
        all_items.append([id, name, description, categories, photos,
                            seller_id, isFlagged, watch_list, quantity])
    
    with open('items.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_items)
    f.close()

def categories():
    category = ["Auto Parts and Accessories", "Automotive Tools & Supplies",
                    "Other Vehicles and Trailers", "Motorcycles",
                    "Powersport Vehicles", "Boats", "Top Vehicle Makes",
                    "Fashion", "Women's Clothing", "Women's Shoes",
                    "Women's Accessories", "Women's Bags & Handbangs",
                    "Men's Clothing", "Men's Shoes", "Men's Accessories",
                    "Kid's Clothing, Shoes, & Accessories", 
                    "Baby Clothing, Shoes, & Accessories", "Jewelry",
                    "Watches, Parts & Accessories"]
    all = []
    for c in category:
        all.append([c])
    with open('category.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all)
    f.close()

def users():
    """
    Creates 30 users

    The id will autoincrement from 1 to n because indexing by integer in mysql is faster + more efficient

    So we won't use `generate_random_id`

    Schema: username, password, email, suspended, is_admin, total_rating, number_of_ratings 
    """
    all_users = []
    existing_usernames = set()

    email_domains = ["@jpmorgan.com", "@uchicago.edu",
                    "@lyft.com"]
    for i in range(0, 30):

        while (True):
            username = get_random_words(3, "_")
            if username not in existing_usernames:
                existing_usernames.add(username)
                break
        # id = generate_random_id()
        email = get_random_words(2, ".") + random.choice(email_domains)
        isAdmin = int(generate_random_bool())
        suspended = int(generate_random_bool())
        password_hash = get_random_words(3, "")
        total_rating = 0
        number_of_ratings = 0
        all_users.append([
            username, password_hash, email, suspended, isAdmin,
            total_rating, number_of_ratings])

    with open('users.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_users)
    f.close()

def auctions():
    """
    generates data for auctions table

    Schema: id, auctionstarttime, auctionendtime, 
            itemid, isBuyNowEnabled, sellerID
    """
    # getting names of items
    file = open("items.csv")
    csvreader = csv.reader(file)
    all_items = []
    for row in csvreader:
        all_items.append((row[0], row[5]))
    file.close()

    auctions = []
    seen_items = set()
    for i in range(0, 30):
        id = generate_random_id()
        auctionstarttime = generate_random_date(datetime.datetime(2021, 10, 23, 0, 0), 
                                    datetime.datetime(2021, 12, 5, 0, 0))
        auctiontime = random.randint(86400, 1814000)
        auctionendtime = str(int(auctionstarttime) + auctiontime)
        while (True):
            itemid, sellerid = random.choice(all_items)
            if itemid not in seen_items:
                seen_items.add(itemid)
                break
        isBuyNowEnabled = generate_random_bool()
        price = round(random.uniform(10.00, 99.99), 2)
        shipping = random.choice([5, 10, 15])
        starting_price = random.choice(list(range(1, int(price))))
        auctions.append([id, auctionstarttime, auctionendtime, itemid, 
                        isBuyNowEnabled, sellerid, price, shipping, starting_price])
    with open('auctions.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(auctions)
    f.close()


def flagged_items():
    """
    This creates the data for the flagged items table

    Schema: id, itemID, flagReason
    """
    # getting names of items
    file = open("items.csv")
    csvreader = csv.reader(file)
    all_items = []
    for row in csvreader:
        all_items.append(row)
    file.close()

    flagReasons = ["Inappropriate", "Counterfeit"]

    all_flagged_items = []
    for i in range(0, 30):
        id = generate_random_id()
        item = random.choice(all_items)
        itemID = item[0]
        item_index = all_items.index(item)
        flagReason = random.choice(flagReasons)
        all_items[item_index][6] = True
        all_flagged_items.append([id, itemID, flagReason])
        
    with open('flagged_items.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_flagged_items)
    f.close()

    with open('items.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_items)
    f.close()

def bids():
    """
    This generates the data for the bids table
    
    schema: id, AuctionID, timestamp, amount, userID
    """
    # getting names of potential bidders
    file = open("users.csv")
    csvreader = csv.reader(file)
    all_users = []
    for row in csvreader:
        all_users.append(row[0])
    file.close()

    # getting auction info
    file = open("auctions.csv")
    csvreader = csv.reader(file)
    all_auctions = []
    for row in csvreader:
        all_auctions.append((row[0], row[1], row[2], row[3], row[5]))
    file.close()

    all_bids = []
    existing_bids = {}
    for i in range(0, 30):
        bid_id = generate_random_id()
        auctionID, auctionstarttime, auctionendtime, itemid, sellerid = random.choice(all_auctions)
        if itemid in existing_bids:
            previous_timestamp = existing_bids[itemid]["Time"]
            previous_bid = existing_bids[itemid]["Amount"]
        else:
            previous_timestamp = 0
            previous_bid = 0
        timestamp = 0
        while int(timestamp) <= int(previous_timestamp):
            timestamp = generate_random_date(datetime.datetime.fromtimestamp(int(auctionstarttime)), 
                                            datetime.datetime.fromtimestamp(int(time.time())))
        amount = 0
        while amount <= previous_bid:
            amount = round(random.uniform(1.00, 100.99), 2)
        if itemid not in existing_bids:
            existing_bids[itemid] = {}
        existing_bids[itemid]["Time"] = timestamp
        existing_bids[itemid]["Amount"] = amount
        userid = random.choice(list(range(1, 31)))
        all_bids.append([bid_id, auctionID, timestamp, amount, userid])
    
    with open('bids.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_bids)
    f.close()

def advertisers():
    """
    This generates data for the advertiser table

    Schema: ID, name, advertiser_category
    """
    advertiser_categories = ["Newspaper/Media", "Finance", "Fashion", "Accomodation and Food Services",
                            "Education", "Leisure and Hospitality", "Public Service", "Health Services",
                            "Arts, Entertainment, Recreation"]
    all_advertisers = []
    for i in range(0, 30):
        advertiser_id = generate_random_id()
        category = random.choice(advertiser_categories)
        name = get_random_words(2, " ")
        all_advertisers.append([advertiser_id, name, category])


    with open('advertisers.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_advertisers)
    f.close()

def advertisements():
    """
    This generates the data for the advertisements table
    Schema: id, content, advertiser_id
    """
    all_advertisers = []
    
    # getting names of advertisers
    file = open("advertisers.csv")
    csvreader = csv.reader(file)
    all_users = []
    for row in csvreader:
        all_advertisers.append(row[0])
    file.close()

    all_advertisements = []
    for i in range(0, 30):
        advertisement_id = generate_random_id()
        content = get_random_words(30, " ")
        advertiser = random.choice(all_advertisers)
        all_advertisements.append([advertisement_id, content, advertiser])
    
    with open('advertisements.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_advertisements)
    f.close()

def notifications():
    """
    This generates the table for the notifications
    schema: id, timestamp, content, recipient
    """
    # getting names of potential sellers
    file = open("users.csv")
    csvreader = csv.reader(file)
    all_users = []
    for row in csvreader:
        all_users.append(row[0])
    file.close()

    all_notifications = []
    for i in range(0, 30):
        id = generate_random_id()
        timestamp = generate_random_date(datetime.datetime(2021, 10, 23, 0, 0), 
                                    datetime.datetime(2021, 12, 31, 0, 0))
        content = get_random_words(30, " ")
        recipient = random.choice(list(range(1, 31)))
        all_notifications.append([id, timestamp, content, recipient])
    

    with open('notifications.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_notifications)
    f.close()

def photos():
    """
    this creates the data for the photos

    schema: id, photo
    """
    all_photos = []
    for i in range(0, 30):
        with open("sample_photos/sample" + str(i) + ".png", "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        id = generate_random_id()
        all_photos.append([id, my_string.decode('utf-8')])
        img_file.close()
    
    with open('photos.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_photos)
    f.close()



def cards():
    """
    Creating credit cards info.

    The user id autoincrements. 

    Schema is user_id, credit card #,
                security code, expiration_date
    """
    # getting names of all users
    file = open("users.csv")
    csvreader = csv.reader(file)
    all_users = []
    for row in csvreader:
        all_users.append(row[0])

    num_users = len(all_users)
    file.close()
    months = list(range(1, 13))
    years = list(range(2022, 2027))

    all_cards = []
    for i in range(1, num_users + 1):
        card = [i]
        card.append(str(random.randint(1111111111111111, 9999999999999999)))
        card.append(str(random.randint(111, 999)))

        # year, month, day
        card.append('{}-{}-{}'.format(random.choice(years), random.choice(months), 1))
        all_cards.append(card)
    
    with open('cards.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_cards)
    f.close()

def carts():
    # getting names of all users
    file = open("users.csv")
    csvreader = csv.reader(file)
    all_users = []
    for row in csvreader:
        all_users.append(row[0])
    
    all_carts = []
    for i in range(0, len(all_users) + 1):
        id = generate_random_id()
        all_carts.append([id, i, []])
    
    with open('carts.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(all_carts)
    f.close()

def watchlist():
    # getting names of items
    file = open("items.csv")
    csvreader = csv.reader(file)
    all_items = []
    for row in csvreader:
        all_items.append(row[0])
    file.close()


    watchlist_examples = []
    for item in all_items:
        seen_users = []
        for i in range(0, 3):
            example = []
            example.append(item)
            user = random.choice(list(range(1, 30)))
            while user in seen_users:
                user = random.choice(list(range(1, 30)))
            example.append(user)
            seen_users.append(user)
            example.append(random.choice(list(range(1, 1000))))
            watchlist_examples.append(example)
    
    with open('watchlist.csv', 'w', newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(watchlist_examples)
    f.close()   



def generate_all_data():
    """
    This generates the random data
    """
    #photos()
    #users()
    #items()
    #categories()
    auctions()
    #flagged_items()
    bids()
    #advertisers()
    #advertisements()
    #notifications()
    #cards()
    #carts()
    #watchlist()

if __name__ == '__main__':
    generate_all_data()







        
