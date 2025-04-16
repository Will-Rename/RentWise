from App.models import Tenant, Review
from App.database import db

#create_tenant
def create_tenant(name, email, password, apartment_id):
    if Tenant.query.filter_by(email=email).first(): 
        return None
    else:
        new_tenant = Tenant(name=name, email=email, password=password, apartment_id=apartment_id)
        db.session.add(new_tenant)
        db.session.commit()
        print(f"Tenant {new_tenant.name} has been created")
        return new_tenant

#create_review
def create_review(tenant_id, apartment_id, review):
    if Tenant.query.get(tenant_id).first(): 
        return None
    else:
        new_review= Review(tenant_id, apartment_id, review)
        db.session.add(new_review)
        db.session.commit()
        print("Tenant created a review")
        return new_review

#get_tenant_reviews
def get_tenant_reviews(tenant_id)