import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from werkzeug.security import generate_password_hash

from App.database import db, get_migrate
from App.models import User, Tenant, Landlord, Apartment, Amenity, ApartmentAmenity, Review
from App.main import create_app
from App.controllers import (
    create_user,
    get_all_users_json,
    get_all_users,
    initialize,
    create_tenant,
    create_landlord,
    create_amenity,
    get_all_amenities,
    create_listing,
    get_apartments,
    list_all_apartments,
    create_review,
    get_tenant_reviews,
    get_apartment_reviews,
    delete_tenant_review,
    delete_amenity,
    get_amenity,
    update_listing,
    delete_listing,
    add_amenity_to_apartment,
    remove_amenity_from_apartment,
    list_apartment_amenities
)

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
@click.option('--name', prompt=True, help="User's name")
@click.option('--email', prompt=True, help="User's email address")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="User's password")
@click.option('--type', type=click.Choice(['tenant', 'landlord'], case_sensitive=False), prompt=True)
@click.option('--phone', help="Phone number (required for landlord)")
def create_user_command(default, name, email, password, type, phone):
    if default:
        name = "testuser"
        email = "test@rentwise.com"
        password = "test123"
        type = "tenant"
        print("Creating default test user...")
    
    user = create_user(name, email, password, type, phone)
    if user:
        print(f"User '{name}' created successfully as {type}.")
    else:
        print("Failed to create user.")

@user_cli.command("list", help="Lists users in the database")
def list_user_command():
    users = get_all_users()
    if not users:
        print("No users found.")
        return
    
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Type: {user.type}")

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
Tenant Commands
'''
tenant_cli = AppGroup('tenant', help='Tenant management commands')

@tenant_cli.command("create", help="Creates a new tenant")
@click.option('--name', prompt=True, help="Tenant's name")
@click.option('--email', prompt=True, help="Tenant's email")
@click.option('--password', prompt=True, hide_input=True, help="Tenant's password")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
def create_tenant_command(name, email, password, apartment_id):
    tenant = create_tenant(name, email, password, apartment_id)
    if tenant:
        print(f"Tenant {tenant.name} created successfully.")
    else:
        print("Failed to create tenant.")

app.cli.add_command(tenant_cli)

'''
Landlord Commands
'''
landlord_cli = AppGroup('landlord', help='Landlord management commands')

@landlord_cli.command("create", help="Creates a new landlord")
@click.option('--name', prompt=True, help="Landlord's name")
@click.option('--email', prompt=True, help="Landlord's email")
@click.option('--password', prompt=True, hide_input=True, help="Landlord's password")
@click.option('--phone', prompt=True, help="Contact phone number")
def create_landlord_command(name, email, password, phone):
    landlord = create_landlord(name, email, password, phone)
    if landlord:
        print(f"Landlord {landlord.name} created successfully.")
    else:
        print("Failed to create landlord.")

app.cli.add_command(landlord_cli)

'''
Amenity Commands
'''
amenity_cli = AppGroup('amenity', help='Amenity management commands')

@amenity_cli.command("create", help="Creates a new amenity")
@click.option('--name', prompt=True, help="Amenity name")
@click.option('--default', is_flag=True, help="Create default amenities")
@click.option('--description', help="Amenity description")
def create_amenity_command(name, default, description):
    if default:
        default_amenities = [
            ("Parking", "Reserved parking spot"),
            ("Pool", "Access to swimming pool"),
            ("Gym", "24/7 fitness center access"),
            ("WiFi", "High-speed internet included"),
            ("Security", "24/7 security system"),
            ("Air Conditioning", "Central AC system"),
            ("Laundry", "In-unit laundry"),
            ("Pet Friendly", "Pets allowed"),
            ("Furnished", "Fully furnished unit")
        ]
        for amenity_name, amenity_desc in default_amenities:
            amenity = create_amenity(amenity_name)
            if amenity:
                print(f"Created default amenity: {amenity_name}")
        return

    amenity = create_amenity(name)
    if amenity:
        print(f"Amenity '{name}' created successfully.")
    else:
        print("Failed to create amenity - amenity may already exist.")

@amenity_cli.command("list", help="Lists all amenities")
def list_amenities_command():
    amenities = get_all_amenities()
    if not amenities:
        print("No amenities found.")
        return
    
    for amenity in amenities:
        print(f"ID: {amenity['amenity_id']}, Name: {amenity['amenity_name']}")

@amenity_cli.command("delete", help="Delete an amenity")
@click.option('--id', type=int, prompt=True, help="Amenity ID")
def delete_amenity_command(id):
    result = delete_amenity(id)
    if result is not None:
        print(f"Amenity deleted successfully.")
    else:
        print("Failed to delete amenity - amenity may not exist.")

@amenity_cli.command("get", help="Get amenity details")
@click.option('--id', type=int, prompt=True, help="Amenity ID")
def get_amenity_command(id):
    amenity = get_amenity(id)
    if amenity:
        print(f"ID: {amenity['amenity_id']}")
        print(f"Name: {amenity['amenity_name']}")
    else:
        print("Amenity not found.")

app.cli.add_command(amenity_cli)

'''
Apartment Commands
'''
apartment_cli = AppGroup('apartment', help='Apartment management commands')

@apartment_cli.command("create", help="Create a new apartment listing")
@click.option('--landlord-id', type=int, prompt=True, help="Landlord ID")
@click.option('--name', prompt=True, help="Apartment name")
@click.option('--location', prompt=True, help="Apartment location")
@click.option('--units-available', type=int, prompt=True, help="Number of available units")
@click.option('--units-total', type=int, prompt=True, help="Total number of units")
@click.option('--details', prompt=True, help="Apartment details")
def create_apartment_command(landlord_id, name, location, units_available, units_total, details):
    units_not_available = units_total - units_available
    if units_not_available < 0:
        print("Error: Available units cannot exceed total units")
        return

    apartment = create_listing(
        landlord_id=landlord_id,
        apartment_name=name,
        apartment_location=location,
        number_of_units_avaliable=units_available,
        number_of_units_not_avaliable=units_not_available,
        apartment_details=details,
        amenities_quantity=[]  # Can be updated later with add-amenity command
    )
    
    if apartment:
        print(f"Apartment '{name}' created successfully.")
    else:
        print("Failed to create apartment listing.")

@apartment_cli.command("list", help="List all apartments")
@click.option('--landlord-id', type=int, help="Filter by landlord ID")
def list_apartments_command(landlord_id):
    apartments = list_all_apartments()
    if not apartments:
        print("No apartments found.")
        return
    
    for apt in apartments:
        if landlord_id and apt.get('landlord_id') != landlord_id:
            continue
        print(f"\nID: {apt['apartment_id']}")
        print(f"Name: {apt['apartment_name']}")
        print(f"Location: {apt['apartment_location']}")
        print(f"Available Units: {apt['number_of_units_avaliable']}")
        print(f"Details: {apt['apartment_details']}")
        print("-" * 40)

@apartment_cli.command("update", help="Update apartment listing")
@click.option('--landlord-id', type=int, prompt=True, help="Landlord ID")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--name', help="New apartment name")
@click.option('--location', help="New apartment location")
@click.option('--units-available', type=int, help="New number of available units")
@click.option('--units-not-available', type=int, help="New number of unavailable units")
@click.option('--details', help="New apartment details")
def update_apartment_command(landlord_id, apartment_id, name, location, units_available, units_not_available, details):
    result = update_listing(
        landlord_id=landlord_id,
        apartment_id=apartment_id,
        apartment_name=name,
        apartment_location=location,
        number_of_units_avaliable=units_available,
        number_of_units_not_avaliable=units_not_available,
        apartment_details=details
    )
    
    if result:
        print("Apartment updated successfully.")
    else:
        print("Failed to update apartment. Check landlord and apartment IDs.")

@apartment_cli.command("delete", help="Delete apartment listing")
@click.option('--landlord-id', type=int, prompt=True, help="Landlord ID")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
def delete_apartment_command(landlord_id, apartment_id):
    result = delete_listing(landlord_id, apartment_id)
    if result:
        print("Apartment deleted successfully.")
    else:
        print("Failed to delete apartment. Check landlord and apartment IDs.")

@apartment_cli.command("add-amenity", help="Add amenity to apartment")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--amenity-id', type=int, prompt=True, help="Amenity ID")
@click.option('--landlord-id', type=int, prompt=True, help="Landlord ID")
@click.option('--quantity', type=int, default=1, help="Quantity of the amenity")
def add_apartment_amenity_command(apartment_id, amenity_id, landlord_id, quantity):
    result = add_amenity_to_apartment(
        apartment_id=apartment_id,
        amenity_id=amenity_id,
        landlord_id=landlord_id,
        quantity=quantity
    )
    if result:
        print(f"Amenity added to apartment successfully.")
    else:
        print("Failed to add amenity to apartment.")

@apartment_cli.command("remove-amenity", help="Remove amenity from apartment")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--amenity-id', type=int, prompt=True, help="Amenity ID")
@click.option('--landlord-id', type=int, prompt=True, help="Landlord ID")
def remove_apartment_amenity_command(apartment_id, amenity_id, landlord_id):
    result = remove_amenity_from_apartment(
        apartment_id=apartment_id,
        amenity_id=amenity_id,
        landlord_id=landlord_id
    )
    if result:
        print("Amenity removed from apartment successfully.")
    else:
        print("Failed to remove amenity from apartment.")

@apartment_cli.command("list-amenities", help="List amenities of an apartment")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
def list_apartment_amenities_command(apartment_id):
    amenities = list_apartment_amenities(apartment_id)
    if not amenities:
        print("No amenities found for this apartment.")
        return
    
    print(f"\nAmenities for Apartment {apartment_id}:")
    for amenity in amenities:
        print(f"- {amenity['amenity_name']} (ID: {amenity['amenity_id']})")

app.cli.add_command(apartment_cli)

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

    found = get_apartments(location, amenity)
    
    if not found:
        print("No apartments found matching your criteria.")
        return

    print("\nFound apartments:")
    for apartment in found:
        print(f"\nID: {apartment['apartment_id']}")
        print(f"Name: {apartment['apartment_name']}")
        print(f"Location: {apartment['apartment_location']}")
        print(f"Available Units: {apartment['number_of_units_avaliable']}")
        print(f"Details: {apartment['apartment_details']}")
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
    review = create_review(tenant_id, apartment_id, review_text)
    if review:
        print(f"Review created successfully for apartment {apartment_id}")
    else:
        print("Failed to create review.")

@review_cli.command("list", help="Lists reviews")
@click.option('--apartment-id', type=int, help="Filter by apartment ID")
@click.option('--tenant-id', type=int, help="Filter by tenant ID")
def list_reviews_command(apartment_id, tenant_id):
    if apartment_id:
        reviews = get_apartment_reviews(apartment_id)
    elif tenant_id:
        reviews = get_tenant_reviews(tenant_id)
    else:
        print("Please provide either apartment-id or tenant-id")
        return
    
    if not reviews:
        print("No reviews found.")
        return
    
    for review in reviews:
        print(f"Review ID: {review['review_id']}")
        print(f"Apartment ID: {review['apartment_id']}")
        print(f"Tenant ID: {review['tenant_id']}")
        print(f"Review: {review['review']}")
        print("---")

@review_cli.command("delete", help="Delete a review")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
@click.option('--review-id', type=int, prompt=True, help="Review ID")
def delete_review_command(tenant_id, review_id):
    result = delete_tenant_review(tenant_id, review_id)
    if result:
        print(f"Review {review_id} deleted successfully.")
    else:
        print("Failed to delete review.")

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