from flask import Flask,make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource

from models import db,Restaurant,RestaurantPizza,PizzaModel

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.json.compact = False

migrate = Migrate(app,db)

db.init_app(app)
api = Api(app)

class Home(Resource):
    def get(self):
        home_response = {"Home":"Restaurant API",}
        response = make_response(jsonify(home_response),200,)
        return response
api.add_resource(Home,'/')

class RestaurantResource(Resource):
    def get(self):
        restaurants = [{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address} for restaurant in Restaurant.query.all()]
        response = make_response(jsonify(restaurants), 200)
        return response
    
api.add_resource(RestaurantResource,'/restaurants')    

class RestaurantByIDResource(Resource):
    def get(self,id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if not restaurant:
            response_dict = {"error": "Restaurant not found"}
            response = make_response(jsonify(response_dict),404)
            return response
        response = make_response(jsonify(restaurant.to_dict()),200)
        return response
    def delete(self,id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if not restaurant:
            response_dict = {"error": "Restaurant not found"}
            response = make_response(jsonify(response_dict),404)
            return response
        db.session.delete(restaurant)
        db.session.commit()
        response_dict = {"deleted":"deleted succesfully"}
        response = make_response(jsonify(response_dict),200)
        return response
api.add_resource(RestaurantByIDResource,'/restaurants/<int:id>') 


class RestaurantPizzaResource(Resource):
    def post(self):
        data = request.get_json()
        restaurantpizza = RestaurantPizza(price= data['price'],pizza_id=data['pizza_id'],restaurant_id= data['restaurant_id'])
        db.session.add(restaurantpizza)
        db.session.commit()
        response= make_response(jsonify(restaurantpizza.to_dict()),201)
        return response

api.add_resource(RestaurantPizzaResource,'/restaurant_pizza')

class PizzaResource(Resource):
    def get(self):
        pizzas = [{'id':pizza.id,'name':pizza.name,'ingredients':pizza.ingredients} for pizza in PizzaModel.query.all()]
        response = make_response(jsonify(pizzas),200)
        return response
api.add_resource(PizzaResource,'/pizza')

if __name__ == '__main__':
    app.run(port=5555, debug=True)