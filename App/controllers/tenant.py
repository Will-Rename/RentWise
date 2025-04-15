from App.models import Tenant
from App.database import db

#create_tenant
def create_tenant(name, email, password, apartment_id):
    if Tenant.query.filter_by(email=email).first(): 
        return None
    
    new_tenant = Tenant(name=name, email=email, password=password, apartment_id=apartment_id)
    db.session.add(new_tenant)
    db.session.commit()
    print(f"Tenant {new_tenant.name} has been created")
    return new_tenant