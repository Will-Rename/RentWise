from App.models import Amenities, ApartmentAmenities, Landlord, Apartment
from App.database import db

#create_amenity
def create_amenity(amenity_name, apartment_id, amenity_id):
    existing_amenity = ApartmentAmenities.query.filter_by(apartment_id=apartment_id, amenity_id=amenity_id).first() 
    if existing_amenity:
        print("This amenity is already present")    
        return None
    else:
        new_amenity = Amenities(amenity_name=amenity_name)
        db.session.add(new_amenity)
        db.session.commit()
        print(f"New amenity {new_amenity.namenity_nameame} has been created")
        return new_amenity

#delete_amenity
def delete_amenity(landlord_id, amenity_id, apartment_id):
    valid_landlord = Landlord.query.get(landlord_id)
    valid_amenity = Amenities.query.get(amenity_id)
    valid_apartment= Apartment.query.get(apartment_id)

    if not valid_apartment:
        print("This is not a valid apartment")
        return None
    
    if not valid_landlord:
        print ("This is not a valid landlord")
        return None

    landlord_apartment = Apartment.query.filter_by(apartment_id=apartment_id, landlord_id=landlord_id).first()
    if not landlord_apartment:
        print("This landlord does not own this apartment")
    
    if valid_amenity is None:
        print ("This is not a valid amenity")
        return None
    
    apartment_amenity = ApartmentAmenities.query.filter_by(apartment_id=apartment_id, amenity_id=amenity_id).first()
    if not apartment_amenity:
        print("The apartment does not own this amenity")
        return None
    

    db.session.delete(amenity_id)
    db.session.commit()
    print(f"The amenity {valid_amenity.amenity_name} was delected from apartment {valid_apartment.apartment_name}")


#get_all_amenities
def get_all_amenities():
    list_of_amenities = Amenities.query.all()
    return list_of_amenities

#get_amenity