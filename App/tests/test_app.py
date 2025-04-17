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
    update_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User(name="bob", email="bob@mail.com", password="bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "name":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)


    
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

    def test_new_apartment(self):
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

        self.landlord = Landlord(
            name='John',
            email='landlord@mail.com',
            password='password',
            phone_number='(868) 123-4567'
        )
        db.session.add(self.landlord)

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
        

