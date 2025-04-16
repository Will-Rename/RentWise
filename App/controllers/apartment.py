from App.models import Apartment, Review, ApartmentAmenities
from App.database import db

#get_apartment
def get_apartment(apartment_id):
    valid_apartment = Apartment.query.get(apartment_id)

    if not valid_apartment:
        print("This is not a vaild apartment")
        return None
    
    print(f"Apartment {valid_apartment.apartment_name} Found")

    apartment= {
        "apartment_id": valid_apartment.apartment_id,
        "apartment_name": valid_apartment.apartment_name,
        "apartment_location": valid_apartment.apartment_location,
        "number_of_units_avaliable": valid_apartment.number_of_units_avaliable,
        "numer_of_units_not_avaliable": valid_apartment.number_of_units_not_avaliable,
        "apartment_details": valid_apartment.apartment_details,
        }
        
    return apartment

#list_all_apartments
def list_all_apartments():
    all_apartments = Apartment.query.all()

    list_of_apartments= [
        {
        "apartment_id": apartment.apartment_id,
        "apartment_name": apartment.apartment_name,
        "apartment_location": apartment.apartment_location,
        "number_of_units_avaliable": apartment.number_of_units_avaliable,
        "numer_of_units_not_avaliable": apartment.number_of_units_not_avaliable,
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
        return None
    
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
        return None
    
    apartment_amenities = ApartmentAmenities.query.filter_by(apartment_id=apartment_id).all()
    
    list_of_apartment_amenities= [
        {
            "amenity_id": amenity.amenity_id,
            "apartment_id": amenity.apartment_id,
            "amenity_name": amenity.amenity_name,
         }
        for amenity in apartment_amenities
    ]
    return list_of_apartment_amenities