from App.models import Apartment
from App.database import db

#get_apartment
def get_apartment(apartment_id):
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        return None
    else:
        return valid_apartment
        