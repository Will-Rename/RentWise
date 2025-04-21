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
    get_all_tenants
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
