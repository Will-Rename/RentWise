from App.models import Apartment, Review
from App.database import db

#get_apartment
def get_apartment(apartment_id):
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        return None
    else:
        print(f"Apartment {valid_apartment.apartment_name} Found")
        return valid_apartment

#list_all_apartments
def list_all_apartments():
    all_apartments = Apartment.query.all()
    return all_apartments

#get_apartment_reviews
def get_apartment_reviews(apartment_id):
    if Apartment.query.get(apartment_id):
        print("This is not a valid apartment") 
        return None
    else:
        apartment_reviews = Review.query.filter_by(apartment_id=apartment_id).all()
        return apartment_reviews

#get_apartment_amenities