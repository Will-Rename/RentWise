#Sample data for testing
from App.models.user import Amenity
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# Create a function to initialize the database
def get_migrate(app):
    return Migrate(app, db)

# Create a function to create the database
def create_db():
  with app.app_context():
    db.create_all()

# Create a function to initialize the database
def init_db(app):
    db.init_app(app)  

def initialize(app):
    with app.app_context():
      from App.models import (User, Tenant, Landlord, Apartment, Amenity, ApartmentAmenity, Review)

#Create Amenities
amenities = [
  Amenity(amenity_name='Wi-Fi'),
  Amenity(amenity_name='Parking'),
  Amenity(amenity_name='Gym')
]
db.session.add_all(amenities)

#Create Landlords then Tenants

landlord = [Landlord(name='John', email='john@email.com', password=generate_password_hash('password123', method='scrypt'), phone_number='123-456-7890'),
            Landlord(name='Jane', email='jane@email.com', password=generate_password_hash('password123', method='scrypt'), phone_number='098-765-4321'),
            Landlord(name='Bob', email='bob@email.com', password=generate_password_hash('bobpass', method='scrypt'), phone_number='111-222-3333')]

tenants = [Tenant(name='Alice', email='alice@email.com', password=generate_password_hash('alicepass', method='scrypt'), apartment_id=1),
           Tenant(name='Bob', email='Jas@email.com', password=generate_password_hash('Jaspass', method='scrypt'), apartment_id=2)]

db.session.add_all(landlord + tenants)

#Create Apartments
Apartments = [Apartment(apartment_name='Apartment 1', apartment_location='123 Sesame St', landlord_id=1, number_of_units_total=10, number_of_units_available=5, number_of_units_not_available=5, apartment_details='One rooms'),
              Apartment(apartment_name='Apartment 2', apartment_location='456 Sesame St', landlord_id=2, number_of_units_total=10, number_of_units_available=5, number_of_units_not_available=5, apartment_details='Two rooms'),
              Apartment(apartment_name='Apartment 3', apartment_location='789 Sesame St', landlord_id=3, number_of_units_total=10, number_of_units_available=5, number_of_units_not_available=5, apartment_details='Three rooms')
              ]
db.session.add_all(Apartments)

db.session.commit()

print ("Sample data added to the database initialized!")