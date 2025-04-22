from App.database import db
from App.controllers.user import create_user
from App.controllers.landlord import create_listing, add_tenant_to_apartment
from App.controllers.tenant import create_review
from App.controllers.amenity import create_amenity

#testing 2/3 main features

'''
Landlord) Create listing with amenities and details
(Verified Tenant) Create review of apartment
'''

def initialize():
    db.drop_all()
    db.create_all()
    
    #Create tenant
    landlord= create_user("jane", "jane@mail.com", "janepass", "landlord", "(868) 622-2002")

    #Create Amenities
    amenity1 =create_amenity("Washer")
    amenity2= create_amenity("TV")     

    #Creating lising
    apartment=create_listing(landlord.user_id, "Sunshine", "St.Augustine", 10, 3, "Easy to find and cozy", [{"amenity_name": "Washer", "quantity": 10}, {"amenity_name": "TV", "quantity": 13}])

    #Create tenant
    tenant= create_user("bob", "bob@mail.com", "bobpass", "tenant", None, apartment_id=apartment.apartment_id)

    #Assigning tenant to an apartment
    add_tenant_to_apartment(tenant.user_id, apartment.apartment_id)

    #Tenant create review
    create_review(tenant.user_id, apartment.apartment_id, "The apartment units are nice and clean")


    
