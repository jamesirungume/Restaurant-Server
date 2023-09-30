from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData,UniqueConstraint,CheckConstraint
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = ('-restaurant_pizzas.restaurant',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', lazy='select')

    __table_args__ = (
        UniqueConstraint('name',name="unique_name_constraint"),
        CheckConstraint('LENGTH(name) <= 50',name="check_name_constraint")
    )
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'pizzas': [pizza.pizza.serialize() for pizza in self.restaurant_pizzas]
        }

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
    serialize_rules = ('-restaurant.restaurant_pizzas',)
    
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('price')
    def validate_price(self, key, price):
        if not (1 < price < 30):
            raise ValueError("price must be between 1 and 30")a
        return price


class PizzaModel(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    
    serialize_rules = ('-restaurant_pizzas.pizza',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', lazy='select')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }
