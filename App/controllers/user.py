from App.models import User, Tenant, Landlord
from App.database import db

def create_user(name, email, password, type, phone_number=None):
    if type not in ["tenant", "landlord"]:
        print(f"This user type {type} is invalid")
        return None
    
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        print("This user already exist")
        return None
    
    if type == "tenant":
        new_user = Tenant(name=name, email=email, password=password)
    elif type == "landlord":
        new_user = Landlord(name=name, email=email, password=password, phone_number=phone_number)
    
    db.session.add(new_user)
    db.session.commit()
    print(f"User {new_user.name} has been created")
    return new_user

def get_user_by_username(username):
    return User.query.filter_by(name=username).first()

def get_user(user_id):
    return User.query.get(user_id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(user_id, username):
    user = get_user(user_id)
    if user:
        user.name = username
        db.session.add(user)
        db.session.commit()
        return user
    return None
