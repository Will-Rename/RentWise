from App.models import Amenity
from App.database import db

#create_amenity
def create_amenity(amenity_name):
    existing_amenity = Amenity.query.filter_by(amenity_name=amenity_name).first() 
    
    if existing_amenity:
        print("This amenity is already present")    
        return None
    
    new_amenity = Amenity(amenity_name=amenity_name)
    db.session.add(new_amenity)
    db.session.commit()
    print(f"New amenity {new_amenity.namenity_nameame} has been created")
    return new_amenity

#delete_amenity
def delete_amenity(amenity_id):
    valid_amenity = Amenity.query.get(amenity_id)
    
    if valid_amenity is None:
        print ("This is not a valid amenity")
        return None
    
    db.session.delete(valid_amenity)
    db.session.commit()
    print(f"The amenity {valid_amenity.amenity_name} was deleted")


#get_all_amenities
def get_all_amenities():
    list_of_amenities = Amenity.query.all()
    return list_of_amenities

#get_amenity
def get_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)

    if not amenity:
        print("This is not valid amenity")
        return None
    
    print(f"Amenity {amenity} was found")
    return amenity