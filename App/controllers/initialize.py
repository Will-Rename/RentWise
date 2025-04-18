from .user import create_user
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user("bob", "bob@mail.com", "bobpass", "tenant")
    create_user("jane", "jane@mail.com", "janepass", "landlord", "(868) 622-2002")
    
