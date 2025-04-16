from App.models import Amenities, ApartmentAmenities
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
    
#update_amenity

#delete_amenity

#get_all_amenities

#get_amenity