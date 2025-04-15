from App.models import Landlord 
from App.database import db

#create_landlord
def create_landlord(name, email, password, phone_contact):
    if Landlord.query.filter_by(email=email).first(): 
        return None
    
    new_landlord = Landlord(name=name, email=email, password=password, phone_contact=phone_contact)
    db.session.add(new_landlord)
    db.session.commit()
    return new_landlord


#create_listing
#update_listing
def update_listing():

#delete_listing
#get_landlord_apartments