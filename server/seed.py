from flask import Flask
from faker import Faker
from models import db, Restaurant, PizzaModel,RestaurantPizza

from app import app
# Initialize the Flask app context
with app.app_context():
    fake = Faker()

    # Function to create fake restaurants
    def create_fake_restaurant():
        restaurant = Restaurant(
            name=fake.unique.first_name(),  # Generates a unique restaurant name
            address=fake.address(),
        )
        db.session.add(restaurant)

    # Function to create fake pizzas
    def create_fake_pizza():
        pizza = PizzaModel(
            name=fake.unique.first_name(),  # Generates a unique pizza name
            ingredients = fake.text(),
        )
        db.session.add(pizza)

    def create_fake_restaurant_pizza():
        restaurant_pizza = RestaurantPizza(
            pizza_id=fake.random_int(min=1, max=20),  # Adjust based on the number of pizzas in your database
            restaurant_id=fake.random_int(min=1, max=10),  # Adjust based on the number of restaurants in your database
            price=fake.random_int(min=1, max=30),  # Generates a random price between 1 and 30
            )
        db.session.add(restaurant_pizza)
    
    # Generate fake data
    db.create_all()
    Faker.seed(0)  # Seed for reproducibility

    # Generate fake restaurants
    for _ in range(10):  # Adjust the number of restaurants you want to generate
        create_fake_restaurant()
        create_fake_restaurant_pizza()

    # Generate fake pizzas
    for _ in range(20):  # Adjust the number of pizzas you want to generate
        create_fake_pizza()

    db.session.commit()
