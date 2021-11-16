import string
import random
import datetime

def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def current_time():
    return float(datetime.datetime.now().timestamp())