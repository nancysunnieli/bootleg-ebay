import string
import random
import datetime
import pprint

def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def current_time():
    return float(datetime.datetime.now().timestamp())

def pretty_print(stuff):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(stuff)