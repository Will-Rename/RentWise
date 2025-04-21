from App.models import Apartment, Review, ApartmentAmenity, Amenity
from App.database import db

#get_apartments using location or amenity - application main feature 3
def get_apartments(location=None, amenity=None):
    found=[]

    if location and not amenity:
        print(f"Searching for apartments using location: {location}")
        found = Apartment.query.filter_by(apartment_location = location).all()

    elif amenity and not location:
        print(f"Searching for apartments using amenity: {amenity}")
        amenity_found= Amenity.query.filter_by(amenity_name=amenity).first()

        if not amenity_found:
            print(f"This amenity: {amenity} was not found")
            return []
        
        amenity_found_apartments = ApartmentAmenity.query.filter_by(amenity_id=amenity_found.amenity_id).all()
        found = [found_location.apartment for found_location in amenity_found_apartments if found_location.apartment]

    elif location and amenity:
        print(f"Searching for aprtment at location {location} with amenity {amenity}")
        amenity_found= Amenity.query.filter_by(amenity_name=amenity).first()

        if not amenity_found:
            print(f"This amenity: {amenity} was not found")
            return []

        found = Apartment.query.join(ApartmentAmenity).filter(Apartment.apartment_location == location, ApartmentAmenity.amenity_id==amenity_found.amenity_id).all()

    else:
        print("No value was entered, enter either the location or amenity or both")
        return []
    
    if not found:
        print("No apartments were found")
        return []

    list_of_found_apartments = []
    for apartments in found:
        list_of_found_apartments.append({
        "apartment_id": apartments.apartment_id,
        "apartment_name": apartments.apartment_name,
        "apartment_location": apartments.apartment_location,
        "number_of_units_available": apartments.number_of_units_available,
        "number_of_units_not_available": apartments.number_of_units_not_available,
        "apartment_details": apartments.apartment_details,
        })
        
    return list_of_found_apartments

#list_all_apartments
def list_all_apartments():
    all_apartments = Apartment.query.all()

    list_of_apartments= [
        {
        "apartment_id": apartment.apartment_id,
        "apartment_name": apartment.apartment_name,
        "apartment_location": apartment.apartment_location,
        "number_of_units_available": apartment.number_of_units_available,
        "number_of_units_not_available": apartment.number_of_units_not_available,
        "apartment_details": apartment.apartment_details,
        }
        for apartment in all_apartments
    ]
    return list_of_apartments

#get_apartment_reviews
def get_apartment_reviews(apartment_id):
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        print("This is not a valid apartment") 
        return []
    
    apartment_reviews = Review.query.filter_by(apartment_id=apartment_id).all()
        
    list_of_apartment_reviews= [
        {
        "review_id": review.review_id,
        "tenant_id": review.tenant_id,
        "apartment_id": review.apartment_id,
        "review": review.review,
        }
        for review in apartment_reviews
    ]
    return list_of_apartment_reviews


#list_apartment_amenities
def list_apartment_amenities(apartment_id):
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        print("This is not a valid Apartment")
        return []
    
    apartment_amenities = ApartmentAmenity.query.filter_by(apartment_id=apartment_id).all()
    
    list_of_apartment_amenities= [
        {
            "amenity_id": a.amenity_id,
            "apartment_id": a.apartment_id,
            "amenity_name": a.amenity.amenity_name,
         }
        for a in apartment_amenities
    ]
    return list_of_apartment_amenities
