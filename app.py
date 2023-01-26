from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={
    r"/*":{'origins':'*'}
})

def mdb(collec_name):
    cluster = MongoClient(os.environ["MONGO_API"])
    db = cluster["e-book"]
    collection = db[collec_name]
    return collection

@app.route('/users', methods=['GET', 'POST'])
def users():
    collection = mdb("users")
    USERS = list(collection.find({}))
    response_object = {}

    if request.method == "POST":
        post_data = request.get_json()
        data = {
            "name" : post_data.get('name'),
            "email" : post_data.get('email'),
            "password" : post_data.get('password'),
            "_id" : len(USERS)+1
        }
        collection.insert_one(data)
        response_object['status'] = 201
    else:
        email = request.args.get('email')
        if email:
            password = request.args.get('password')
            if password:
                for user in USERS:
                    if user['email'] == email and user['password'] == password:
                        response_object = [user]
        else:
            response_object = list(mdb("users").find({}))

    return jsonify(response_object)


@app.route('/books', methods=['GET', 'POST'])
def books():
    collection = mdb("books")
    BOOKS = list(collection.find({}))
    response_object = {}

    if request.method == "POST":
        post_data = request.get_json()
        data = {
            "name" : post_data.get('name'),
            "rating" : post_data.get('rating'),
            "author" : post_data.get('author'),
            "_id" : len(BOOKS)+1
        }
        collection.insert_one(data)
        response_object['status'] = 201
    elif request.method == "GET":
        _id = request.args.get('_id')
        try:
            _id = int(_id)
        except:
            _id = _id
        if _id:
            for book in BOOKS:
                if book['_id'] == _id:
                    response_object = [book]
        else:
            response_object = BOOKS

    return jsonify(response_object)


@app.route('/books/<int:_id>', methods=['PUT'])
def update_books(_id):
    collection = mdb("books")
    BOOKS = list(collection.find({}))
    if request.method == "PUT":
        post_data = request.get_json()
        for book in BOOKS:
            if book['_id'] == _id:
                post_data['_id'] = _id
                filter = { '_id': _id}
                newvalues = { "$set": post_data}
                collection.update_one(filter, newvalues)
                response = [post_data]


    return jsonify(response)


if __name__=="__main__":
    app.run(debug=False,host='0.0.0.0')
