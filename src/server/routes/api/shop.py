from flask import jsonify, Blueprint, request
from server.services.database.db import users as Users
from server.services.database.db import get_user_item_buy

list_item = {

}

route_shop = Blueprint("api-shop", __name__)

@route_shop.route("/<int:user_id>")
def shop_list(user_id):
    list_return = {}
    for item in list_item:
        if item not in get_user_item_buy():
            list_return+=item
    return list_return

@route_shop.route("/<int:user_id>")
def item_buy(user_id):
    return get_user_item_buy()

