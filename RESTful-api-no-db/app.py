# =============== START NOTES HTTP Status Code  =============== 
# Most common HTTP status code: 200 (server returns data, as we wanted, all OK)
# 201 (for created)
# 202 (accepted delaying the creation (ex: object created after 5-10 mins))
# 404 (means not found)
# 400 bad request

# Ex:
# (For POST) return item, 201
# (For GET) return {'item': item}, 200 if item else 404
# =============== END NOTES HTTP Status Code  =============== 

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
# flask_jwt for authentication
# User will be an entity that has a unique identifying number and username and pass.
# client sends us username and password, we send them jwt(Jason web token).
# The JWT will be the user id. Once client has jwt they can send data to us letting us know they have prev been authenticated.

from security import authenticate, identity

# NOTE: Flask restful jsonifies for you, you can just return dictionaries, to return JSON



app = Flask(__name__) # unique name for Flask to use

app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
# Inorder to encrypt and understand what is being encrypted we need a key
# in production this must be secured and hidden
# It is used to encode the cookies and JWT so that users cannot modify them on their browser.
app.secret_key = 'samplesecretkey'

api = Api(app) # allow us to easily add resources

# use our authenticate, identity functions for auth of users
# jwt creates a new endpoint /auth, where we send username and password
# username and password are sent over to authenticate func, which returns the user and that becomes the identity
# !!!: the auth endpoint returns a jwt token (we then send the jwt token to the next request we make), jwt calls 
# the identiy function, uses the jwt token to get the correct userid that the jwt token represents (if it can do that, user was authenticated)
jwt = JWT(app, authenticate, identity)

items = []


# Two resources:
# Class Item
# Class ItemList

# For operations: 
# Items: get
# Item<name>: get, post,delete,put

class Item(Resource):
    # Class Variables
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    # note: To post to that jwt method we send in header with auth info
    # Authorization   JWT <whole token>
    # decorator to auth before calling get
    #@jwt_required()
    def get(self, name):

        # filter() returns a filter object. 
        # next() gets first item found by filter function (can call next again to get 2nd, 3rd, ...)
        # next breaks if no next item. so if next func doesnt find item, return none instead

        # get item with requested name
        item = next(filter(lambda x: x['name'] == name, items), None);
        # 200 if item exists, else 404 HTTP status code
        return {'item': item}, 200 if item else 404

        # simpler:
        #return {'item': next(filter(lambda x: x['name'] == name, items), None)}

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            # if item exists and is not None
            # client should have checked if item already exists, return bad request
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        #data=request.get_json(force=True) # will format to jsson even if content type not set to application/json
        #data=request.get_json(silent=True) # returns none if header content type not set to application/json
        # 

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item

    #@jwt_required()
    def delete(self, name):
        global items # tell python the outer var in this block is the outer items var
        # overwrite our items list with a new list without that item
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    # create or update item
    #@jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            # use dictionary update method
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    #app.run(port=5000, debug=True)  # important to mention debug=True
    app.run(port=5000, debug=True)  # important to mention debug=True
