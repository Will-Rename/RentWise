from App.models import User, Tenant, Landlord
from App.database import db

#def create_user(username, password):
def create_user(name, email, password, type):
    if type not in ["tenant", "landlord"]:
        return None
    
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        print("This user already exist")
        return None
    
    if type == "tenant":
        new_user = Tenant(name=name, email=email, password=password)
    elif type == "landlord":
        new_user = Landlord(name=name, email=email, password=password, phone_contact=phone_contact)
    
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    