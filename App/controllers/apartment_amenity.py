from App.models import ApartmentAmenities, Apartment, Amenity
from App.database import db

#add_amenity_to_apartment
def add_amenity_to_apartment(apartment_id, quantity, amenity_id, landlord_id):
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        print ("This is not a valid apartment")
        return None
    
    if valid_apartment.landlord_id != landlord_id:
        print("This landlord is not authorized to add amenities to this apartment")
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
def remove_amenity_from_apartment(apartment_id, amenity_id, landlord_id):
    valid_apartment_amenity = ApartmentAmenities.query.filter_by(apartment_id=apartment_id, amenity_id=amenity_id).first()
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        print ("This is not a valid apartment")
        return None

    if valid_apartment.landlord_id != landlord_id:
        print("This landlord is not authorized to remove amenities to this apartment")
        return None
    
    if not valid_apartment_amenity:
        print ("This is Apartment does not have this amenity")
        return None
    
    db.session.delete(valid_apartment_amenity)
    db.session.commit()
    print(f"Amenity {amenity_id.amenity_name} has been removed from apartment {apartment_id.apartment_name}")
    