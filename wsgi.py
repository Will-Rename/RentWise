import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
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
    delete_tenant_review
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
@click.option('--default', is_flag=True, help="Create default amenities")
@click.option('--name', prompt=True, help="Amenity name")
def create_amenity_command(default, name):
    if default:
        default_amenities = [
            "Parking",
            "Pool",
            "Gym",
            "WiFi",
            "Security"
        ]
        for amenity_name in default_amenities:
            amenity = create_amenity(amenity_name)
            if amenity:
                print(f"Created default amenity: {amenity_name}")
        return

    amenity = create_amenity(name)
    if amenity:
        print(f"Amenity '{name}' created successfully.")
    else:
        print("Failed to create amenity.")

@amenity_cli.command("list", help="Lists all amenities")
def list_amenities_command():
    amenities = get_all_amenities()
    if not amenities:
        print("No amenities found.")
        return
    
    for amenity in amenities:
        print(f"ID: {amenity['amenity_id']}, Name: {amenity['amenity_name']}")

app.cli.add_command(amenity_cli)

'''
Search Commands
'''
search_cli = AppGroup('search', help='Search commands')

@search_cli.command("apartments", help="Search for apartments")
@click.option('--location', help="Search by location")
@click.option('--amenity', help="Search by amenity name")
def search_apartments_command(location, amenity):
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