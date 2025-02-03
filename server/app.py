#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource # type: ignore
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# Get the restaurants
@app.route('/restaurants', methods = ['GET'])
def get_restaurants():
    
    restaurant = Restaurant.query.all()
    #created an empty list 
    restaurant_list= [
        {
           "id":rest.id, 
           "name":rest.name,
           "address":rest.address 
        }for rest in restaurant  
    ]
    
    return jsonify({"Restaurants_list": restaurant_list})
    
    
@app.route('/restaurants/<int:id>', methods= ['GET'])
def get_one_restaurant(id):
    rest = Restaurant.query.filter_by(id=id).first()
    if rest:
        return jsonify({
            "id":rest.id, 
           "name":rest.name,
           "address":rest.address    
        })
    else: 
        return jsonify({"error": "Restaurant not found"})
    
    
@app.route('/restaurants/<int:id>', methods = ['DELETE'])
def del_restaurant(id):
    delete_restaurant = Restaurant.query.get(id)
    
    if delete_restaurant: 
        db.session.delete(delete_restaurant)
        db.session.commit()
        return jsonify({"Success": "Restaurant was deleted"})
    else: 
        return jsonify({"error": "Restaurant not found"})
    
#get pizza 
@app.route('/pizzas', methods = ['GET'])
def get_pizza():
    pizza = Pizza.query.all()
    pizz_list = []
    for p in pizza:
        pizz_list.append({
            "id":p.id,
            "name":p.name,
            "ingredients":p.ingredients
        })
        return jsonify({"Pizza": pizz_list})
    
#Post the pizza 
@app.route('/restaurant_pizzas', methods = ['POST'])
def restaurant_pizza():
    # get the pizza
    data = request.get_json()
    price = data['price']
    pizza_id = data['pizza_id']
    restaurant_id= data['restaurant_id']
    
    
    check_pizza_id = Pizza.query.filter_by(id=pizza_id).first()
    check_restaurant_id = Restaurant.query.filter_by(id=restaurant_id).first()

    
    if not check_pizza_id or not check_restaurant_id: 
        return jsonify({"errors": ["validation errors"]})
    else: 
        new_restaurant = RestaurantPizza(price=price,pizza_id=pizza_id,restaurant_id=restaurant_id)
        db.session.add(new_restaurant)
        db.session.commit()
        return jsonify({"Success":"Restaurant created"})
    
     
if __name__ == "__main__":
    app.run(port=5555, debug=True)
