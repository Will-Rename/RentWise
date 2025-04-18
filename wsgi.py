import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from werkzeug.security import generate_password_hash

from App.database import db, get_migrate
from App.models import User, Tenant, Landlord, Apartment, Amenity, ApartmentAmenity, Review
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )

app = create_app()
migrate = get_migrate(app)

# Database initialization commands
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')

'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a user")
@click.option('--default', is_flag=True, help="Create a default test user")
@click.option('--username', prompt=True, help="User's username")
@click.option('--email', prompt=True, help="User's email address")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="User's password")
def create_user_command(default, username, email, password):
    if default:
        username = "testuser"
        email = "test@rentwise.com"
        password = "test123"
        print("Creating default test user...")
    
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    print(f"User '{username}' created successfully.")

@user_cli.command("list", help="Lists users in the database")
def list_users_command():
    users = User.query.all()
    if not users:
        print("No users found.")
        return
    
    for user in users:
        role = "Admin" if user.is_admin else "Regular"
        status = "Active" if user.is_active else "Inactive"
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {role}, Status: {status}")

app.cli.add_command(user_cli)

'''
Auth Commands
'''
auth_cli = AppGroup('auth', help='Authentication commands')

@auth_cli.command("create-admin", help="Creates a new admin user")
@click.option('--default', is_flag=True, help="Create a default admin user")
@click.option('--username', prompt=True, help="Admin username")
@click.option('--email', prompt=True, help="Admin email")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="Admin password")
def create_admin_command(default, username, email, password):
    if default:
        username = "admin"
        email = "admin@rentwise.com"
        password = "admin123"
        print("Creating default admin user...")
    
    hashed_password = generate_password_hash(password)
    admin = User(username=username, email=email, password=hashed_password, is_admin=True)
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user '{username}' created successfully.")

app.cli.add_command(auth_cli)

'''
Landlord Commands
'''
landlord_cli = AppGroup('landlord', help='Landlord management commands')

@landlord_cli.command("create", help="Creates a new landlord profile")
@click.option('--default', is_flag=True, help="Create a default landlord profile")
@click.option('--user-id', type=int, prompt=True, help="Associated user ID")
@click.option('--phone', prompt=True, help="Contact phone number")
def create_landlord_command(default, user_id, phone):
    if default:
        default_user = User(
            username="landlord",
            email="landlord@rentwise.com",
            password=generate_password_hash("landlord123")
        )
        db.session.add(default_user)
        db.session.flush()
        user_id = default_user.id
        phone = "555-0100"
        print("Creating default landlord profile...")

    landlord = Landlord(user_id=user_id, phone=phone)
    db.session.add(landlord)
    db.session.commit()
    print(f"Landlord profile created for user ID {user_id}")

@landlord_cli.command("list", help="Lists all landlords")
def list_landlords_command():
    landlords = Landlord.query.join(User).all()
    if not landlords:
        print("No landlords found.")
        return
    
    for landlord in landlords:
        print(f"ID: {landlord.id}, User: {landlord.user.username}, Phone: {landlord.phone}")

app.cli.add_command(landlord_cli)

'''
Tenant Commands
'''
tenant_cli = AppGroup('tenant', help='Tenant management commands')

@tenant_cli.command("create", help="Creates a new tenant profile")
@click.option('--default', is_flag=True, help="Create a default tenant profile")
@click.option('--user-id', type=int, prompt=True, help="Associated user ID")
@click.option('--phone', prompt=True, help="Contact phone number")
def create_tenant_command(default, user_id, phone):
    if default:
        default_user = User(
            username="tenant",
            email="tenant@rentwise.com",
            password=generate_password_hash("tenant123")
        )
        db.session.add(default_user)
        db.session.flush()
        user_id = default_user.id
        phone = "555-0200"
        print("Creating default tenant profile...")

    tenant = Tenant(user_id=user_id, phone=phone)
    db.session.add(tenant)
    db.session.commit()
    print(f"Tenant profile created for user ID {user_id}")

@tenant_cli.command("list", help="Lists all tenants")
def list_tenants_command():
    tenants = Tenant.query.join(User).all()
    if not tenants:
        print("No tenants found.")
        return
    
    for tenant in tenants:
        print(f"ID: {tenant.id}, User: {tenant.user.username}, Phone: {tenant.phone}")

app.cli.add_command(tenant_cli)

'''
Apartment Commands
'''
apartment_cli = AppGroup('apartment', help='Apartment management commands')

@apartment_cli.command("create", help="Creates a new apartment listing")
@click.option('--default', is_flag=True, help="Create a default apartment")
@click.option('--address', prompt=True, help="Apartment address")
@click.option('--rent', type=float, prompt=True, help="Monthly rent")
@click.option('--landlord-id', type=int, prompt=True, help="Landlord ID")
@click.option('--description', prompt=True, help="Apartment description")
def create_apartment_command(default, address, rent, landlord_id, description):
    if default:
        address = "123 Main St"
        rent = 1200.00
        landlord = Landlord.query.first()
        if not landlord:
            print("Error: No landlord found in the system. Create a landlord first.")
            return
        landlord_id = landlord.id
        description = "Modern 2-bedroom apartment"
        print("Creating default apartment...")

    apartment = Apartment(
        address=address,
        rent=rent,
        landlord_id=landlord_id,
        description=description
    )
    db.session.add(apartment)
    db.session.commit()
    print(f"Apartment at '{address}' created successfully.")

@apartment_cli.command("list", help="Lists all apartments")
@click.option('--landlord-id', type=int, help="Filter by landlord ID")
def list_apartments_command(landlord_id):
    query = Apartment.query
    if landlord_id:
        query = query.filter_by(landlord_id=landlord_id)
    
    apartments = query.all()
    if not apartments:
        print("No apartments found.")
        return
    
    for apt in apartments:
        print(f"ID: {apt.id}, Address: {apt.address}, Rent: ${apt.rent:.2f}")
        print(f"Description: {apt.description}")
        print("---")

app.cli.add_command(apartment_cli)

'''
Amenity Commands
'''
amenity_cli = AppGroup('amenity', help='Amenity management commands')

@amenity_cli.command("create", help="Creates a new amenity")
@click.option('--default', is_flag=True, help="Create default amenities")
@click.option('--name', prompt=True, help="Amenity name")
@click.option('--description', prompt=True, help="Amenity description")
def create_amenity_command(default, name, description):
    if default:
        default_amenities = [
            ("Parking", "Reserved parking spot"),
            ("Pool", "Access to swimming pool"),
            ("Gym", "24/7 fitness center access"),
            ("WiFi", "High-speed internet included"),
            ("Security", "24/7 security system")
        ]
        for amenity_name, amenity_desc in default_amenities:
            amenity = Amenity(name=amenity_name, description=amenity_desc)
            db.session.add(amenity)
        db.session.commit()
        print("Default amenities created successfully.")
        return

    amenity = Amenity(name=name, description=description)
    db.session.add(amenity)
    db.session.commit()
    print(f"Amenity '{name}' created successfully.")

@amenity_cli.command("list", help="Lists all amenities")
def list_amenities_command():
    amenities = Amenity.query.all()
    if not amenities:
        print("No amenities found.")
        return
    
    for amenity in amenities:
        print(f"ID: {amenity.id}, Name: {amenity.name}")
        print(f"Description: {amenity.description}")
        print("---")

app.cli.add_command(amenity_cli)

'''
Search Commands
'''
search_cli = AppGroup('search', help='Search commands')

@search_cli.command("apartments", help="Search for apartments")
@click.option('--location', help="Search by location")
@click.option('--amenity', help="Search by amenity name")
def search_apartments_command(location, amenity):
    if not location and not amenity:
        print("Please provide either location or amenity to search.")
        return

    found = []
    
    if location and not amenity:
        print(f"Searching for apartments in location: {location}")
        found = Apartment.query.filter_by(apartment_location=location).all()
    elif amenity and not location:
        print(f"Searching for apartments with amenity: {amenity}")
        amenity_found = Amenity.query.filter_by(amenity_name=amenity).first()
        if not amenity_found:
            print(f"Amenity '{amenity}' not found.")
            return
        amenity_found_apartments = ApartmentAmenity.query.filter_by(amenity_id=amenity_found.id).all()
        found = [apt_amenity.apartment for apt_amenity in amenity_found_apartments if apt_amenity.apartment]
    elif location and amenity:
        print(f"Searching for apartments in {location} with amenity: {amenity}")
        amenity_found = Amenity.query.filter_by(amenity_name=amenity).first()
        if not amenity_found:
            print(f"Amenity '{amenity}' not found.")
            return
        found = Apartment.query.join(ApartmentAmenity).filter(
            Apartment.apartment_location == location,
            ApartmentAmenity.amenity_id == amenity_found.id
        ).all()

    if not found:
        print("No apartments found matching your criteria.")
        return

    print("\nFound apartments:")
    for apartment in found:
        print(f"\nID: {apartment.id}")
        print(f"Name: {apartment.apartment_name}")
        print(f"Location: {apartment.apartment_location}")
        print(f"Available Units: {apartment.number_of_units_available}")
        print(f"Details: {apartment.apartment_details}")
        print("-" * 40)

app.cli.add_command(search_cli)

'''
Review Commands
'''
review_cli = AppGroup('review', help='Review management commands')

@review_cli.command("create", help="Creates a new review")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--review-text', prompt=True, help="Review text")
def create_review_command(tenant_id, apartment_id, review_text):
    tenant = Tenant.query.get(tenant_id)
    apartment = Apartment.query.get(apartment_id)
    
    if not tenant:
        print("Tenant not found.")
        return
    
    if not apartment:
        print("Apartment not found.")
        return

    review = Review(
        tenant_id=tenant_id,
        apartment_id=apartment_id,
        review_text=review_text
    )
    db.session.add(review)
    db.session.commit()
    print(f"Review created successfully for apartment {apartment_id}")

@review_cli.command("list", help="Lists reviews")
@click.option('--apartment-id', type=int, help="Filter by apartment ID")
@click.option('--tenant-id', type=int, help="Filter by tenant ID")
def list_reviews_command(apartment_id, tenant_id):
    query = Review.query
    if apartment_id:
        query = query.filter_by(apartment_id=apartment_id)
    if tenant_id:
        query = query.filter_by(tenant_id=tenant_id)
    
    reviews = query.all()
    if not reviews:
        print("No reviews found.")
        return
    
    for review in reviews:
        print(f"Review ID: {review.id}")
        print(f"Apartment ID: {review.apartment_id}")
        print(f"Tenant ID: {review.tenant_id}")
        print(f"Review: {review.review_text}")
        print("---")

app.cli.add_command(review_cli)

'''
Test Commands
'''
test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)