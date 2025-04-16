from App.models import ApartmentAmenities, Apartment, Amenity
from App.database import db

#add_amenity_to_apartment
def add_amenity_to_apartment(apartment_id, quantity, amenity_id):
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        print ("This is not a valid apartment")
        return None
    
    existing_amenity = Amenity.query.get(amenity_id) 
    if not existing_amenity:
        print("This amenity does not exist")    
        return None
    
    new_apartment_amenity = ApartmentAmenities(apartment_id=apartment_id, amenity_id=amenity_id, quantity=quantity)
    db.session.add(new_apartment_amenity)
    db.session.commit()
    print(f"New amenity {existing_amenity.amenity_name} has been added to apartment {valid_apartment.apartment_name}")
    return new_apartment_amenity

#remove_amenity_from_apartment
def remove_amenity_from_apartment(apartment_id, amenity_id):
    valid_apartment_amenity = ApartmentAmenities.query.filter_by(apartment_id=apartment_id, amenity_id=amenity_id).first()

    if not valid_apartment_amenity:
        print ("This is Apartment does not have this amenity")
        return None
    else:
        db.session.delete(valid_apartment_amenity)
        db.session.commit()
        print(f"Amenity {amenity_id.amenity_name} has been removed from apartment {apartment_id.apartment_name}")
        

#get_apartment_amenities
def get_apartment_amenities (apartment_id):
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        print("This is nt a valid apartment")
        return None
    
    apartment_amenities = ApartmentAmenities.query.all(apartment_id)
    return apartment_amenities