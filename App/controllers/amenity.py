from App.models import Amenity
from App.database import db

#create_amenity
def create_amenity(amenity_name):
    existing_amenity = Amenity.query.filter_by(amenity_name=amenity_name).first() 
    
    if existing_amenity:
        print(f"This amenity: {amenity_name} is already present")    
        return None
    
    new_amenity = Amenity(amenity_name=amenity_name)
    db.session.add(new_amenity)
    db.session.commit()
    print(f"New amenity {new_amenity.amenity_name} has been created")
    return new_amenity

#delete_amenity
def delete_amenity(amenity_id):
    valid_amenity = Amenity.query.get(amenity_id)
    
    if not valid_amenity:
        print (f"The amenity with id: {amenity_id} was not found")
        return None
    
    if valid_amenity.apartment_amenities:
        print(f"Cannot delete amenity {valid_amenity.amenity_name} is presently in use")
        return None

    db.session.delete(valid_amenity)
    db.session.commit()
    print(f"The amenity {valid_amenity.amenity_name} was deleted")
    return valid_amenity

#get_all_amenities
def get_all_amenities():
    list_of_amenities = Amenity.query.all()

    amenities= [
        {
            "amenity_id": amenity.amenity_id,
            "amenity_name": amenity.amenity_name,
        }
        for amenity in list_of_amenities
    ]
    return amenities

#get_amenity
def get_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)

    if not amenity:
        print (f"The amenity with id: {amenity_id} was not found")
        return None
    
    print(f"Amenity {amenity} was found")
    return {
            "amenity_id": amenity.amenity_id,
            "amenity_name": amenity.amenity_name,
        }