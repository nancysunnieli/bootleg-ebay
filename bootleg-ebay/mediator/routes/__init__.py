from flask import Blueprint
routes = Blueprint('routes', __name__)

from .items import *
from .users import *
from .auctions import *
from .carts import *
from .payments import *