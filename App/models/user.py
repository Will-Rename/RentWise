from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = "user"
 
    user_id = db.Column(db.Integer, unique=True, primary_key=True)
    name =  db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50)) 
    
    __mapper_args__ ={
        "polymorphic_identity": "user",
        'polymorphic_on': type
    }
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)
    
    def get_json(self):
        return{
            'id': self.user_id,
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
        return f'<User id: {self.user_id} name: {self.name} email: {self.email}>'

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.apartment_id'), nullable=False)
    
    #Relationship
    reviews = db.relationship('Review', backref='tenant', lazy=True, primaryjoin= "Tenant.user_id == Review.tenant_id")

    __mapper_args__ = {
        'polymorphic_identity': 'tenant',
    }

    def create_review(self, apartment_id, review_text):
        review = Review(review_text=review_text,
                        apartment_id=apartment_id,
                        tenant_id=self.user_id
        )
        db.session.add(review)
        db.session.commit()
        print (f"Tenant {self.user_id} created a review")
        return review

    def __init__(self, name, email, password, apartment_id):
        super().__init__(name=name, email=email, password=password)
        self.apartment_id= apartment_id

    def __repr__(self):
        return f'<Tenant {self.user_id} : {self.name} - {self.email}>'


class Landlord(User):
    __tablename__ = 'landlord'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False, unique=True) # String format of 0 (000) 000-0000.
    
    #Relationship
    apartments = db.relationship('Apartment', backref='landlord', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'landlord',
    }

    def create_listing(self, name, location, units_available, units_not_available, apartment_details, amenities_quantity):
        apartment = Apartment(landlord_id=self.user_id,
                            apartment_name=name,
                            apartment_location=location,
                            number_of_units_available=units_available,
                            number_of_units_not_available=units_not_available,
                            apartment_details=apartment_details,
        )
        db.session.add(apartment)
        db.session.commit()

        print(f"Apartment Listing for {apartment.apartment_name} has been created")

        for amenity in amenities_quantity:
            amenity_name = amenity.get("amenity_name") #from Amenity class
            quantity = amenity.get("quantity", 1) #from ApartmentAmenities class

            existing_amenity= Amenity.query.filter_by(amenity_name=amenity_name).first()

            if not existing_amenity:
                print(f"The amenity {amenity_name} does not currently exist")
                continue
            
            from App.controllers import add_amenity_to_apartment
            add_amenity_to_apartment(apartment_id=apartment.apartment_id, quantity=quantity, amenity_id=existing_amenity.amenity_id, landlord_id=self.user_id) #function in ApartmentAmenities controller

        return apartment

    def __init__(self, name, email, password, phone_number):
        super().__init__(name=name, email=email, password=password)
        self.phone_number= phone_number

    def __repr__(self):
        return f'<Landlord {self.user_id} : {self.name} - {self.email}>'


class Apartment(db.Model):
    __tablename__ = 'apartment'

    apartment_id = db.Column(db.Integer, primary_key=True)
    apartment_name = db.Column(db.String(100), nullable=False)
    apartment_location = db.Column(db.String(100), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.user_id'), nullable=False)
    #number_of_units_total = db.Column(db.Integer, nullable=False) # Total number of units in the apartment.
    number_of_units_available = db.Column(db.Integer, nullable=False)
    number_of_units_not_available = db.Column(db.Integer, nullable=False)
    apartment_details = db.Column(db.String(200), nullable=False)

    # Relationships
    tenants = db.relationship('Tenant', backref='apartment', lazy=True)
    reviews = db.relationship('Review', backref='apartment', lazy=True)
    amenities = db.relationship('ApartmentAmenity', backref='apartment', lazy=True)
    
    def __repr__(self):
        return f'<Apartment {self.apartment_id} - Name: {self.apartment_name} Location: {self.apartment_location}>'


class Amenity(db.Model):
    __tablename__ = 'amenity'

    amenity_id = db.Column(db.Integer, primary_key=True)
    amenity_name = db.Column(db.String(100), nullable=False)
    
    #Relationship
    apartment_amenities = db.relationship('ApartmentAmenity', backref='amenity', lazy=True)

    def __repr__(self):
        return f'<Amenity {self.amenity_id} : {self.amenity_name}>'
    

class ApartmentAmenity(db.Model):
    __tablename__ = 'apartment_amenity'
    #id = db.Column(db.Integer, primary_key=True)

    #Composite Key
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.apartment_id'), nullable=False, primary_key=True)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenity.amenity_id'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default = 1) # Quantity of the amenity in the apartment.

    def __repr__(self):
        return f'<ApartmentAmenity {self.apartment_id} - {self.amenity_id}: qty = {self.quantity}>'


class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String(200), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.apartment_id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.user_id'), nullable=False)

    def __repr__(self):
        return f'<Review {self.review_id} : {self.review_text} Creator : {self.tenant_id}>'
    
