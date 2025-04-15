from App.models import Landlord, Apartment
from App.database import db

#create_landlord
def create_landlord(name, email, password, phone_contact):
    if Landlord.query.filter_by(email=email).first(): 
        return None
    
    new_landlord = Landlord(name=name, email=email, password=password, phone_contact=phone_contact)
    db.session.add(new_landlord)
    db.session.commit()
    return new_landlord


#create_listing
def create_listing(landlord_id, apartment_name, apartment_location, number_of_units_avaliable, number_of_units_not_avaliable, apartment_details):
    valid_landlord = Landlord.query.get(landlord_id)
    if not valid_landlord:
        return None
    else:
        new_apartment = Apartment(apartment_name=apartment_name, apartment_location=apartment_location, number_of_units_avaliable=number_of_units_avaliable, number_of_units_not_avaliable=number_of_units_not_avaliable, apartment_details=apartment_details)
        db.session.add(new_apartment)
        db.session.commit()
        return new_apartment
    
#update_listing
def update_listing():

#delete_listing
#get_landlord_apartments