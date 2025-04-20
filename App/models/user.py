from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))
    __mapper_args__ ={
        'polymorphic_on': type
    }

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method = 'scrypt')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.name} - {self.email}>'

    def __get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'type': self.type
        }

class Tenant(User):
    __tablename__ = 'tenant'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    reviews = db.relationship('Review', backref='tenant', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'tenant',
    }

    def create_review(self, apartment_id, review_text):
        review = Review(review_text=review_text,
                        apartment_id=apartment_id,
                        tenant_id=self.id
        )
        db.session.add(review)
        db.session.commit()
        return review

    def __repr__(self):
        return f'<Tenant {self.id} : {self.name} - {self.email}>'

class Landlord(User):
    __tablename__ = 'landlord'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False, unique=True) # String format of 0 (000) 000-0000.
    apartments = db.relationship('Apartment', backref='landlord', lazy=True)
    __mapper_args__ = {
        'polymorphic_identity': 'landlord',
    }

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

    def __repr__(self):
        return f'<Landlord {self.id} : {self.name} - {self.email}>'

class Apartment(db.Model):
    __tablename__ = 'apartment'
    id = db.Column(db.Integer, primary_key=True)
    apartment_name = db.Column(db.String(100), nullable=False)
    apartment_location = db.Column(db.String(100), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)
    number_of_units_total = db.Column(db.Integer, nullable=False) # Total number of units in the apartment.
    number_of_units_available = db.Column(db.Integer, nullable=False)
    number_of_units_not_available = db.Column(db.Integer, nullable=False)
    apartment_details = db.Column(db.String(200), nullable=False)

    # Relationships
    tenants = db.relationship('Tenant', backref='apartment', lazy=True)
    reviews = db.relationship('Review', backref='apartment', lazy=True)
    amenities = db.relationship('ApartmentAmenity', backref='apartment', lazy=True)

    def __repr__(self):
        return f'<Apartment {self.id} : {self.apartment_name} - {self.apartment_location}>'

class Amenity(db.Model):
    __tablename__ = 'amenity'
    id = db.Column(db.Integer, primary_key=True)
    amenity_name = db.Column(db.String(100), nullable=False)
    apartment_amenities = db.relationship('ApartmentAmenity', backref='amenity', lazy=True)

    def __repr__(self):
        return f'<Amenity {self.id} : {self.amenity_name}>'

class ApartmentAmenity(db.Model):
    __tablename__ = 'apartment_amenity'
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenity.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default = 1) # Quantity of the amenity in the apartment.

    def __repr__(self):
        return f'<ApartmentAmenity {self.apartment_id} - {self.amenity_id}: qty = {self.quantity}>'

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String(200), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)

    def __repr__(self):
        return f'<Review {self.id} : {self.review_text}>'
    
