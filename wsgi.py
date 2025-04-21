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
    create_landlord,
    create_tenant,
    get_all_landlords,
    get_all_tenants,
    create_amenity,
    get_all_amenities,
    get_amenity,
    delete_amenity,
    create_listing,
    list_all_apartments,
    get_apartments,
    list_apartment_amenities,
    get_apartment_reviews,
    create_review,
    get_tenant_reviews,
    delete_tenant_review
)

app = create_app()
migrate = get_migrate(app)

@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')

'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)

'''
Landlord Commands
'''
landlord_cli = AppGroup('landlord', help='Landlord object commands')

@landlord_cli.command("create", help="Creates a landlord")
@click.argument("username", default="landlord")
@click.argument("password", default="landpass")
def create_landlord_command(username, password):
    create_landlord(username, password)
    print(f'Landlord {username} created!')

@landlord_cli.command("list", help="Lists all landlords")
def list_landlords_command():
    print(get_all_landlords())

app.cli.add_command(landlord_cli)

'''
Tenant Commands
'''
tenant_cli = AppGroup('tenant', help='Tenant object commands')

@tenant_cli.command("create", help="Creates a tenant")
@click.argument("username", default="tenant")
@click.argument("password", default="tenantpass")
def create_tenant_command(username, password):
    create_tenant(username, password)
    print(f'Tenant {username} created!')

@tenant_cli.command("list", help="Lists all tenants")
def list_tenants_command():
    print(get_all_tenants())

app.cli.add_command(tenant_cli)

'''
Amenity Commands
'''
amenity_cli = AppGroup('amenity', help='Amenity object commands')

@amenity_cli.command("create", help="Creates a new amenity")
@click.argument("name", required=True)
def create_amenity_command(name):
    amenity = create_amenity(name)
    if amenity:
        print(f'Amenity {name} created!')

@amenity_cli.command("list", help="Lists all amenities")
def list_amenities_command():
    print(get_all_amenities())

@amenity_cli.command("get", help="Get an amenity by ID")
@click.argument("id", type=int)
def get_amenity_command(id):
    amenity = get_amenity(id)
    print(amenity)

@amenity_cli.command("delete", help="Delete an amenity by ID")
@click.argument("id", type=int)
def delete_amenity_command(id):
    delete_amenity(id)

app.cli.add_command(amenity_cli)

'''
Apartment Commands
'''
apartment_cli = AppGroup('apartment', help='Apartment object commands')

@apartment_cli.command("create", help="Creates a new apartment listing")
@click.option("--landlord-id", required=True, type=int, help="ID of the landlord")
@click.option("--name", required=True, help="Name of the apartment")
@click.option("--location", required=True, help="Location of the apartment")
@click.option("--units-available", required=True, type=int, help="Number of available units")
@click.option("--units-not-available", required=True, type=int, help="Number of unavailable units")
@click.option("--details", required=True, help="Details about the apartment")
def create_apartment_command(landlord_id, name, location, units_available, units_not_available, details):
    apartment = create_listing(landlord_id, name, location, units_available, units_not_available, details, [])
    if apartment:
        print(f'Apartment listing {name} created!')

@apartment_cli.command("list", help="Lists all apartments or filtered by landlord")
@click.option("--landlord-id", type=int, help="Filter by landlord ID")
def list_apartments_command(landlord_id):
    apartments = list_all_apartments()
    print(apartments)

@apartment_cli.command("search", help="Search apartments by location or amenity")
@click.option("--location", help="Location to search for")
@click.option("--amenity", help="Amenity to search for")
def search_apartments_command(location, amenity):
    apartments = get_apartments(location, amenity)
    print(apartments)

@apartment_cli.command("list-amenities", help="List amenities for an apartment")
@click.argument("apartment-id", type=int)
def list_apartment_amenities_command(apartment_id):
    amenities = list_apartment_amenities(apartment_id)
    print(amenities)

app.cli.add_command(apartment_cli)

'''
Review Commands
'''
review_cli = AppGroup('review', help='Review object commands')

@review_cli.command("create", help="Creates a new review")
@click.option("--tenant-id", required=True, type=int, help="ID of the tenant")
@click.option("--apartment-id", required=True, type=int, help="ID of the apartment")
@click.option("--review-text", required=True, help="The review text")
def create_review_command(tenant_id, apartment_id, review_text):
    review = create_review(tenant_id, apartment_id, review_text)
    if review:
        print(f'Review created for apartment {apartment_id}!')

@review_cli.command("list", help="Lists reviews by apartment or tenant")
@click.option("--apartment-id", type=int, help="Filter by apartment ID")
@click.option("--tenant-id", type=int, help="Filter by tenant ID")
def list_reviews_command(apartment_id, tenant_id):
    if apartment_id:
        reviews = get_apartment_reviews(apartment_id)
    elif tenant_id:
        reviews = get_tenant_reviews(tenant_id)
    else:
        print("Please provide either --apartment-id or --tenant-id")
        return
    print(reviews)

@review_cli.command("delete", help="Delete a review")
@click.option("--tenant-id", required=True, type=int, help="ID of the tenant")
@click.option("--review-id", required=True, type=int, help="ID of the review to delete")
def delete_review_command(tenant_id, review_id):
    delete_tenant_review(tenant_id, review_id)

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
    elif type == "landlord":
        sys.exit(pytest.main(["-k", "LandlordIntegrationTest"]))
    elif type == "tenant":
        sys.exit(pytest.main(["-k", "TenantIntegrationTest"]))
    elif type == "search":
        sys.exit(pytest.main(["-k", "SearchIntegrationTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
