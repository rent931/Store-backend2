

from flask import Flask, request, abort
from mock_data import catalog
import json
import random

app = Flask("Main")
me = {
        "name": "Miguel",
        "last": "Renteria",
        "age": 28,
        "hobbies": [],
        "address": {
            "street": "Evergreen",
            "number": 118,
            "city": "Springfield"
        }
    }

@app.route("/", methods=['GET'])
def home():
    return "Hello from Python"


@app.route("/test")
def any_name():
    return "I'm a test function"


@app.route("/about")
def about():
    return me["name"] + " " + me["last"]




#*******************************************************
#************************** API Endpoints **************
#*******************************************************

@app.route("/api/catalog")
def get_catalog():
    # TODO: Read the catalog from the database
    return json.dumps(catalog)


@app.route("/api/catalog", methods=["post"])
def save_product():
    product = request.get_json()
    print(product)


    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "Title is required, & should be at least 5 character long")

    if not "price" in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should be a valid number")
    

    if product["price"] <= 0:
        return abort(400, "Price should be greater than zero")

    product["_id"] = random.randint(1000, 100000)

    catalog.append(product)

    return json.dumps(product)


@app.route("/api/cheapest")
def get_cheapest():

    cheap = catalog[0]
    for product in catalog:
        if product["price"] < cheap["price"]:
            cheap = product
    

    return json.dumps(cheap)


@app.route("/api/product/<id>")
def get_product(id):
    for product in catalog:
        if product["_id"] == id:
            return json.dumps(product)
    

    return "NOT FOUND"



@app.route("/api/catalog/<category>")
def get_by_category(category):
    result = []
    for product in catalog:
        if product["category"].lower() == category.lower():
            result.append(product)

    return json.dumps(result)



@app.route("/api/categories")
def get_categories():
    result = []
    for product in catalog:
        cat = product["category"]
        if cat not in result:
            result.append(cat)

    return json.dumps(result)



app.run(debug=True, port=5001)
