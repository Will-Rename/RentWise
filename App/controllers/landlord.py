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
def update_listing(landlord_id, apartment_id, apartment_name=None, apartment_location=None, number_of_units_avaliable=None, number_of_units_not_avaliable=None, apartment_details=None):
    valid_landlord = Landlord.query.get(landlord_id)
    valid_apartment = Apartment.query.get(apartment_id)

    if valid_landlord is not valid_apartment.landlord_id:
        return None
    else:
        if apartment_name:
            valid_apartment.apartment_name = apartment_name

        if apartment_location:
            valid_apartment.apartment_location = apartment_location

        if number_of_units_avaliable:
            valid_apartment.number_of_units_avaliable = number_of_units_avaliable
        
        if number_of_units_not_avaliable:
            valid_apartment.number_of_units_not_avaliable = number_of_units_not_avaliable

        if apartment_details:
            valid_apartment.apartment_details = apartment_details

        db.session.commit()

#delete_listing
#get_landlord_apartments