import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from modelos.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This filed cannot be left blank')
    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occurred while trying to find the name"}, 500
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "item with name {} already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data["price"])
        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {"message": "Item {} deleted".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item"}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item"}, 500
        return updated_item.json()


class Itemlist(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        result = cursor.execute(query, )
        rows = result.fetchall()
        items = []
        for item in rows:
            items.append({'name': item[0], 'price': item[1]})

        return {'items': items}
