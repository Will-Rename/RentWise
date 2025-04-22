from App.models import User, Landlord, Apartment, Amenity, Tenant
from App.controllers.apartment_amenity import add_amenity_to_apartment
from App.database import db

'''
#create_landlord
def create_landlord(name, email, password, phone_number):
    if User.query.filter_by(email=email).first(): 
        print("Email is already taken") 
        return None
    else:
        new_landlord = Landlord(name=name, email=email, password=password, phone_contact=phone_contact)
        db.session.add(new_landlord)
        db.session.commit()
        print(f"Landlord {new_landlord.name} has been created")
        return new_landlord
'''

#create_listing with amenities and details - application main feature 1
def create_listing(landlord_id, apartment_name, apartment_location, number_of_units_avaliable, number_of_units_not_avaliable, apartment_details, amenities_quantity):
    valid_landlord = Landlord.query.get(landlord_id)
    
    if not valid_landlord:
        print("This is not a valid landlord")
        return None

    new_apartment = Apartment(apartment_name=apartment_name, apartment_location=apartment_location, number_of_units_available=number_of_units_avaliable, number_of_units_not_available=number_of_units_not_avaliable, apartment_details=apartment_details, landlord_id=landlord_id)
    db.session.add(new_apartment)
    db.session.commit()
    print(f"Apartment Listing for {new_apartment.apartment_name} has been created")

    for amenity in amenities_quantity:
        amenity_name = amenity.get("amenity_name")
        quantity = amenity.get("quantity", 1)

        existing_amenity= Amenity.query.filter_by(amenity_name=amenity_name).first()

        if not existing_amenity:
            print(f"The amenity {amenity_name} does not currently exist")
            continue

        add_amenity_to_apartment(apartment_id=new_apartment.apartment_id, quantity=quantity, amenity_id=existing_amenity.amenity_id, landlord_id=landlord_id)

    return new_apartment
    
    
#update_listing
def update_listing(landlord_id, apartment_id, apartment_name=None, apartment_location=None, number_of_units_available=None, number_of_units_not_available=None, apartment_details=None):
    valid_landlord = Landlord.query.get(landlord_id)
    valid_apartment = Apartment.query.get(apartment_id)

    if valid_landlord is None:
        print("This is not a valid landlord")
        return None
    
    if valid_apartment is None:
        print("This is not a valid apartment")
        return None
    
    if valid_landlord.user_id != valid_apartment.landlord_id:
        print("This landlord is not authorized to update this listing")
        return None
    
    if apartment_name:
        valid_apartment.apartment_name = apartment_name

    if apartment_location:
        valid_apartment.apartment_location = apartment_location

    if number_of_units_available:
        valid_apartment.number_of_units_available = number_of_units_available
        
    if number_of_units_not_available:
        valid_apartment.number_of_units_not_available = number_of_units_not_available

    if apartment_details:
        valid_apartment.apartment_details = apartment_details

    db.session.commit()
    print(f"Apartment Listing for {valid_apartment.apartment_name} has been updated")
    return valid_apartment

#delete_listing
def delete_listing(landlord_id, apartment_id):
    valid_landlord = Landlord.query.get(landlord_id)
    valid_apartment = Apartment.query.get(apartment_id)

    if valid_landlord is None:
        print("This is not a valid landlord")
        return None
    
    if valid_apartment is None:
        print("This is not a valid apartment")
        return None
    
    if valid_landlord.user_id != valid_apartment.landlord_id:
        print("This landlord is not authorized to delete this listing")
        return None
    
    db.session.delete(valid_apartment)
    db.session.commit()
    print(f"Apartment Listing for {valid_apartment.apartment_name} has been deleted")
    return valid_apartment

#get_landlord_apartments
def get_landlord_apartments(landlord_id):
    valid_landlord = Landlord.query.get(landlord_id)
    
    if not valid_landlord:
        print("This is not a valid landlord")
        return None
    
    landlord_apartments = Apartment.query.filter_by(landlord_id=landlord_id).all()
    
    list_of_landlord_apartments= [
        {
        "apartment_id": apartment.apartment_id,
        "apartment_name": apartment.apartment_name,
        "apartment_location": apartment.apartment_location,
        "number_of_units_avaliable": apartment.number_of_units_avaliable,
        "numer_of_units_not_avaliable": apartment.number_of_units_not_avaliable,
        "apartment_details": apartment.apartment_details,
        }
        for apartment in landlord_apartments
    ]
    return list_of_landlord_apartments

#add tenant to an apartment
def add_tenant_to_apartment(tenant_id, apartment_id):
    valid_tenant = Tenant.query.get(tenant_id)

    if not valid_tenant:
        print ("This user is not a valid tenant")
        return None
    
    valid_tenant.apartment_id = apartment_id
    db.session.commit()
    print("New tenant added to an apartment")
    return valid_tenant
