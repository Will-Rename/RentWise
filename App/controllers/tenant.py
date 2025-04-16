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
    if Tenant.query.get(tenant_id): 
        return None
    else:
        new_review= Review(tenant_id, apartment_id, review)
        db.session.add(new_review)
        db.session.commit()
        print("Tenant created a review")
        return new_review

#get_tenant_reviews
def get_tenant_reviews(tenant_id):
    if Tenant.query.get(tenant_id): 
        return None
    else:
        tenant_reviews = Review.query.filter_by(tenant_id=tenant_id).all()
        return tenant_reviews

#delete_tenant_review
def delete_tenant_review(tenant_id, review_id):
    valid_tenant = Tenant.query.get(tenant_id)
    valid_review = Review.query.get(review_id)

    if valid_tenant is None:
        print ("This is not a valid tenant")
        return None

    if valid_review is None:
        print ("This is not a valid review")
        return None
    
    if valid_tenant is valid_review.tenant_id:
        db.session.delete(review_id)
        db.session.commit()
        print(f"Tenant {valid_tenant.name} delected review {valid_review}")
