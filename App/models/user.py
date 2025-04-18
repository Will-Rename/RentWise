from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__= "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))
    
    __mapper_args__ ={
        'polymorphic_identity': "user",
        "polymorphic_on": type
    }

    def __init__(self, name, email, password, type):
        self.name = name
        self.email = email
        self.set_password(password)
        self.type= type

    def get_json(self):
        return{
            'user_id': self.user_id,
            'name': self.name,
            "email": self.email,
            "type": self.type
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method = 'scrypt')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User name: {self.name} email: {self.email} type: {self.type}>'

    '''
    def __get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'type': self.type
        }
    '''

class Tenant(User):
    __tablename__ = 'tenant'
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.apartment_id'), nullable=False)
    
    #Relationships
    reviews = db.relationship('Review', backref='tenant', lazy=True)
    apartment= db.relationship('Apartment', backref='tenant', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'tenant'
    }
    
    '''
    def create_review(self, apartment_id, review_text):
        review = Review(review_text=review_text,
                        apartment_id=apartment_id,
                        tenant_id=self.id
        )
        db.session.add(review)
        db.session.commit()
        return review
    '''

    def __init__(self, name, email, password):
        super().__init__(name, email, password, type="tenant")

    def get_json(self):
        return{
            'tenant_id': self.tenant_id,
            'name': self.name,
            "email": self.email,
            "type": self.type
        }
    
    def __repr__(self):
        return f'<Tenant {self.tenant_id} : {self.name} - {self.email}>'
    

class Landlord(User):
    __tablename__ = 'landlord'
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False, unique=True) # String format of 0 (000) 000-0000.
    
    #Relationships
    apartments = db.relationship('Apartment', backref='landlord', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'landlord'
    }

    '''
    def create_listing(self, name, location, total_units, units_available, apartment_details):
        apartment = Apartment(apartment_id = self.id,
                              landlord_id=self.id,
                            apartment_name=name,
                            apartment_location=location,
                            number_of_units_total=total_units,
                            number_of_units_available=units_available,
                            number_of_units_not_available=units_available,
                            apartment_details=apartment_details
        )
        db.session.add(apartment)
        db.session.commit()
        return apartment
    '''
    def __init__(self, name, email, password, phone_number):
        super().__init__(name, email, password, type="landlord")
        self.phone_number= phone_number

    def get_json(self):
        return{
            'landlord_id': self.landlord_id,
            'name': self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "type": self.type
        }
    
    def __repr__(self):
        return f'<Landlord {self.landlord_id} : {self.name} - {self.email} {self.phone_number}>'


class Apartment(db.Model):
    __tablename__ = 'apartment'
    apartment_id = db.Column(db.Integer, primary_key=True)
    apartment_name = db.Column(db.String(100), nullable=False)
    apartment_location = db.Column(db.String(100), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.landlord_id'), nullable=False)
    #number_of_units_total = db.Column(db.Integer, nullable=False) # Total number of units in the apartment.
    number_of_units_available = db.Column(db.Integer, nullable=False)
    number_of_units_not_available = db.Column(db.Integer, nullable=False)
    apartment_details = db.Column(db.String(200), nullable=False)

    # Relationships
    #tenants = db.relationship('Tenant', backref='apartment', lazy=True)
    reviews = db.relationship('Review', backref='apartment', lazy=True)
    apartment_amenities = db.relationship('ApartmentAmenity', backref='apartment', lazy=True)
    #landlord= db.relationship("Landlord", backref="apartment", lazy=True)

    def __init__ (self, apartment_name, apartment_location, landlord_id, number_of_units_available, number_of_units_not_available, apartment_details):
        self.apartment_name = apartment_name
        self.apartment_location = apartment_location
        self.landlord_id = landlord_id #not too sure about this part
        self.number_of_units_available = number_of_units_available
        self.number_of_units_not_available = number_of_units_not_available
        self.apartment_details = apartment_details

    def __repr__(self):
        return f'<Apartment {self.apartment_id} : {self.apartment_name} - {self.apartment_location} Number of units avaliable {self.number_of_units_available}>'

    def get_json(self):
        return{
            'apartment_id': self.apartment_id,
            'apartment_name': self.apartment_name,
            "apartment_location": self.apartment_location,
            "number_of_units_available": self.number_of_units_available,
            "apartment_details": self.apartment_details
        }
    
class Amenity(db.Model):
    __tablename__ = 'amenity'
    amenity_id = db.Column(db.Integer, primary_key=True)
    amenity_name = db.Column(db.String(100), nullable=False)
    
    #Relationship
    amenity_apartment = db.relationship('ApartmentAmenity', backref="amenity", lazy=True)

    def __init__ (self, amenity_name):
        self.amenity_name = amenity_name

    def __repr__(self):
        return f'<Amenity {self.amenity_id} : {self.amenity_name}>'
    

class ApartmentAmenity(db.Model):
    __tablename__ = 'apartment_amenity'
    #id = db.Column(db.Integer, primary_key=True)
    #Composite Key
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.apartment_id'), primary_key=True)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenity.amenity_id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default = 1) # Quantity of the amenity in the apartment.

    #Relationships
    #amenity_apartment= db.relationship("Apartment", backref="amenity", lazy=True)
    #apartment_amenities= db.relationship('ApartmentAmenity', backref="apartment", lazy=True)

    def __repr__(self):
        return f'<ApartmentAmenity {self.apartment_id} - {self.amenity_id} Quantity = {self.quantity}>'


class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String(200), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.apartment_id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.tenant_id'), nullable=False)

    def __init__ (self, tenant_id, apartment_id, review_text):
        self.tenant_id= tenant_id
        self.apartment_id= apartment_id
        self.review_text= review_text

    def get_json(self):
        return{
            "tenant_id": self.tenant_id,
            "apartment_id": self.apartment_id,
            "review": self.review_text
        }
    
    def __repr__(self):
        return f'<Review {self.review_id} : {self.review_text}>'
    