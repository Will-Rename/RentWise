from App.models import Apartment
from App.database import db

#get_apartment
def get_apartment(apartment_id):
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        return None
    else:
        print("Apartment Found")
        return valid_apartment

#list_all_apartments
def list_all_apartments():
    all_apartments = Apartment.query.all()
    return all_apartments