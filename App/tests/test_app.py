import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Tenant, Landlord, Apartment, Amenity, ApartmentAmenity, Review
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    create_amenity,
    create_listing,
    add_tenant_to_apartment,
    create_review
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.client = self.app.test_client()
        with self.app.app_context():
            create_db()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_new_user(self):
        user = User(name="bob", email="bob@test.com", password="bobpass")
        assert user.name == "bob"
        assert user.email == "bob@test.com"
        assert user.check_password("bobpass")

    def test_get_json(self):
        user = User(name="bob", email="bob@test.com", password="bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {
            "id": None,
            "name": "bob",
            "email": "bob@test.com",
            "type": None
        })
    
    def test_hashed_password(self):
        password = "mypass"
        user = User(name="bob", email="bob@test.com", password=password)
        db.session.add(user)
        db.session.commit()
        assert user.password != password
        self.assertTrue(user.password.startswith('scrypt$'))

    def test_check_password(self):
        password = "mypass"
        user = User(name="bob", email="bob@test.com", password=password)
        db.session.add(user)
        db.session.commit()
        assert user.check_password(password)
        assert not user.check_password("wrongpassword")


    
class ApartmentUnitTests(unittest.TestCase):

    def test_new_apartment(self):
        self.landlord = Landlord(
            name='John',
            email='landlord@mail.com',
            password='password',
            phone_number='(868) 123-4567'
        )
        db.session.add(self.landlord)
        db.session.commit()

        apartment = Apartment(
            apartment_name='Test_Apartment',
            apartment_location='Test_Location',
            landlord_id=self.landlord.id,
            number_of_units_total=10,
            number_of_units_available=5,
            number_of_units_not_available=5,
            apartment_details='Test_Details'
        )
        db.session.add(apartment)
        db.session.commit()

        assert apartment.apartment_name == "Test_Apartment"
        assert apartment.landlord_id == self.landlord.id
        assert apartment.number_of_units_total == 10
        assert apartment.landlord == self.landlord


    def test_apartment_units_logic(self):
        """Test unit availability logic"""
        apartment = Apartment(
            apartment_name='Test_Apartment',
            apartment_location='Test_Location',
            landlord_id=self.landlord.id,
            number_of_units_total=15,
            number_of_units_available=10,
            number_of_units_not_available=5,
            apartment_details='Test_Details'
        )
        db.session.add(apartment)
        db.session.commit()

        assert apartment.number_of_units_total == apartment.number_of_units_available + apartment.number_of_units_not_available



class TenantUnitTests(unittest.TestCase):

    def create_test_tenants(self):

        self.landlord = Landlord(
            name='John',
            email='landlord@mail.com',
            password='password',
            phone_number='(868) 123-4567'
        )
        db.session.add(self.landlord)
        db.session.commit()

        self.apartment = Apartment(
            apartment_name='Test_Apartment',
            apartment_location='Test_Location',
            landlord_id=self.landlord.id,
            number_of_units_total=10,
            number_of_units_available=9,
            number_of_units_not_available=1,
            apartment_details='Test_Details'
        )
        db.session.add(self.apartment)
        db.session.commit()

        tenant = Tenant(
            name='Jane Doe',
            email='jane@mail.com',
            password='password',
            apartment_id=self.apartment.id
        )
        db.session.add(tenant)
        db.session.commit()

        assert tenant.name  == 'Jane Doe'
        assert tenant.email == 'jane@mail.com'
        assert tenant.check_password('password') == 'password'
        assert tenant.apartment_id, self.apartment.id
        assert tenant.apartment == self.apartment

        assert self.apartment.number_of_units_available == 8
        assert self.apartment.number_of_units_not_available == 2

    def test_tenant_json(self):
        #Test tenant get_json
        tenant = Tenant(
            name='Jason',
            email='json@mail.com',
            password='password',
            apartment_id=self.apartment.id
        )
        db.session.add(tenant)
        db.session.commit()
       
        tenant_json = tenant.get_json()
        
        assert tenant_json['id'] == tenant.id
        assert tenant_json['name'] == 'Jason'
        assert tenant_json['email'] == 'json@mail.com'
        assert tenant_json['type'] == 'tenant'
        assert tenant_json['apartment_id'] == self.apartment.id



class AmentitiesUnitTests(unittest.TestCase):
    def test_create_amenity(self, init_db):

        # Test basic amenity creation
        amenity = Amenity(amenity_name='Swimming Pool')
        db.session.add(amenity)
        db.session.commit()

        assert amenity.id is not None
        assert amenity.amenity_name == 'Swimming Pool'
        assert len(amenity.apartment_amenities) == 0

    def test_amenity_apartment_relationship(self):
    
        # Create test apartment
        apartment = Apartment(
            apartment_name='Luxury Apartments',
            apartment_location='Beachfront',
            landlord_id=1,  
            number_of_units_total=20,
            number_of_units_available=10,
            number_of_units_not_available=10,
            apartment_details='Luxury beachfront living'
        )

        # Create amenity
        amenity = Amenity(amenity_name='Gym')
        db.session.add_all([apartment, amenity])
        
        # Create relationship
        apartment_amenity = ApartmentAmenity(
            apartment_id=apartment.id,
            amenity_id=amenity.id,
            quantity=2
        )
        db.session.add(apartment_amenity)
        db.session.commit()

        # Test relationships
        assert len(amenity.apartment_amenities) == 1
        assert amenity.apartment_amenities[0].apartment == apartment
        assert amenity.apartment_amenities[0].quantity == 2

    def test_amenity_json(self):
        # Test amenity JSON representation
        amenity = Amenity(amenity_name='Parking')
        db.session.add(amenity)
        db.session.commit()
        
        amenity_json = amenity.get_json()
        assert amenity_json['id'] == amenity.id
        assert amenity_json['amenity_name'] == 'Parking'

class ReviewUnitTests(unittest.TestCase):

    def setup(self):
        """Setup test data for reviews"""
        # Create landlord
        self.landlord = Landlord(
            name='John Smith',
            email='john@example.com',
            password='password',
            phone_number='(555) 123-4567'
        )
        
        # Create apartment
        self.apartment = Apartment(
            apartment_name='City View',
            apartment_location='Downtown',
            landlord_id=self.landlord.id,
            number_of_units_total=50,
            number_of_units_available=25,
            number_of_units_not_available=25,
            apartment_details='Modern downtown living'
        )

        # Create tenant
        self.tenant = Tenant(
            name='Jane Doe',
            email='jane@example.com',
            password='password',
            apartment_id=self.apartment.id
        )
        db.session.add_all([self.landlord, self.apartment, self.tenant])
        db.session.commit()


        assert review.id is not None
        assert review.review_text == 'Great location and amenities!'
        assert review.apartment == self.apartment
        assert review.tenant == self.tenant
        assert review.date_created is not None

    def test_review_relationships(self):
        """Test review relationships"""
        review = Review(
            review_text='Could be cleaner in common areas',
            apartment_id=self.apartment.id,
            tenant_id=self.tenant.id
        )
        db.session.add(review)
        db.session.commit()

        # Test apartment 
        assert len(self.apartment.reviews) == 1
        assert self.apartment.reviews[0] == review
        
        # Test tenant
        assert len(self.tenant.reviews) == 1
        assert self.tenant.reviews[0] == review

    def test_review_json(self):
        # Test review JSON representation
        review = Review(
            review_text='Overall good experience',
            apartment_id=self.apartment.id,
            tenant_id=self.tenant.id
        )
        db.session.add(review)
        db.session.commit()
        
        review_json = review.get_json()
        assert review_json['id'] == review.id
        assert review_json['review_text'] == 'Overall good experience'
        assert review_json['apartment_id'] == self.apartment.id
        assert review_json['tenant_id'] == self.tenant.id



'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


#Test in terminal using: pytest -k "LandlordIntegrationTest" 
class LandlordIntegrationTest(unittest.TestCase):
    
    def test_create_listing_with_amenities_and_details(self):
        
        landlord= create_user("john", "john@mail.com", "johnpass", "landlord", "(868) 123-4567")
        
        login("john", "johnpass")

        create_amenity("Large Pool")
        create_amenity("Parking")     

        apartment=create_listing(landlord.user_id, "Apartment2", "Arima", 15, 2, "Safe environment", [{"amenity_name": "Large Pool", "quantity": 1}, {"amenity_name": "Parking", "quantity": 20}])

        self.assertEqual(apartment.apartment_location, "Arima")
        self.assertEqual(len(apartment.amenities),2)
        self.assertEqual(apartment.landlord_id, landlord.user_id)


#
class TenantIntegrationTest(unittest.TestCase):

    def test_create_review_of_apartment(self):
        
        landlord= create_user("sam", "sam@mail.com", "sampass", "landlord", "(868) 891-0111")

        create_amenity("2 Large Bed Rooms")
        create_amenity("Large Yard")     

        apartment3=create_listing(landlord.user_id, "Apartment3", "Barataria", 10, 8, "Luxury apartments", [{"amenity_name": "2 Large Bed Rooms", "quantity": 18}, {"amenity_name": "Large Yard", "quantity": 1}])

        tenant= create_user("smith", "smith@mail.com", "smithpass", "tenant", None, apartment_id=apartment3.apartment_id)

        add_tenant_to_apartment(tenant.user_id, apartment3.apartment_id)

        review= create_review(tenant.user_id, apartment3.apartment_id, "Beautiful apartment complex")

        self.assertEqual(apartment3.apartment_location, "Barataria")
        self.assertEqual(len(apartment3.amenities),2)
        self.assertEqual(apartment3.landlord_id, landlord.user_id)
        self.assertEqual(tenant.name, "smith")
        self.assertEqual(review.apartment_id, apartment3.apartment_id)
        







 
        

