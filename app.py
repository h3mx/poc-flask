from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import identity, authenticate
from resources.user import UserRegister
from resources.item import Item, Itemlist

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "gabito"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Itemlist, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)