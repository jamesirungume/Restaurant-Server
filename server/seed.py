from flask import Flask
from faker import Faker
from models import db, Restaurant, PizzaModel,RestaurantPizza

from app import app

with app.app_context():
    fake = Faker()

   
    def create_fake_restaurant():
        restaurant = Restaurant(
            name=fake.unique.first_name(),  # Generates a unique restaurant name
            address=fake.address(),
        )
        db.session.add(restaurant)

   
    def create_fake_pizza():
        pizza = PizzaModel(
            name=fake.unique.first_name(),
            ingredients = fake.text(),
        )
        db.session.add(pizza)

    def create_fake_restaurant_pizza():
        restaurant_pizza = RestaurantPizza(
            pizza_id=fake.random_int(min=1, max=20),  \
            restaurant_id=fake.random_int(min=1, max=10),  
            price=fake.random_int(min=1, max=30),  
            )
        db.session.add(restaurant_pizza)
    
    
    db.create_all()
    Faker.seed(0)  

   
    for _ in range(10):  
        create_fake_restaurant()
        create_fake_restaurant_pizza()

   
    for _ in range(20):  
        create_fake_pizza()

    db.session.commit()
