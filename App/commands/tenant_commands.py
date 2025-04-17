import click
from models import db, Tenant, User
from app import app
from werkzeug.security import generate_password_hash

@app.cli.command("create-tenant")
@click.option('--default', is_flag=True, help="Create a default tenant profile")
@click.option('--user-id', type=int, prompt=True, help="Associated user ID")
@click.option('--phone', prompt=True, help="Contact phone number")
def create_tenant(default, user_id, phone):
    """Creates a new tenant profile."""
    if default:
        # Create a default user first
        default_user = User(
            username="tenant",
            email="tenant@rentwise.com",
            password=generate_password_hash("tenant123")
        )
        db.session.add(default_user)
        db.session.flush()
        user_id = default_user.id
        phone = "555-0200"
        click.echo("Creating default tenant profile...")

    tenant = Tenant(user_id=user_id, phone=phone)
    db.session.add(tenant)
    db.session.commit()
    click.echo(f"Tenant profile created for user ID {user_id}")

@app.cli.command("list-tenants")
def list_tenants():
    """List all tenants."""
    tenants = Tenant.query.join(User).all()
    if not tenants:
        click.echo("No tenants found.")
        return
    
    for tenant in tenants:
        click.echo(f"ID: {tenant.id}, User: {tenant.user.username}, Phone: {tenant.phone}")

@app.cli.command("update-tenant-phone")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
@click.option('--phone', prompt=True, help="New phone number")
def update_tenant_phone(tenant_id, phone):
    """Update a tenant's phone number."""
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        click.echo("Tenant not found.")
        return
    
    tenant.phone = phone
    db.session.commit()
    click.echo(f"Phone number updated for tenant ID {tenant_id}")

@app.cli.command("delete-tenant")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
@click.confirmation_option(prompt="Are you sure you want to delete this tenant?")
def delete_tenant(tenant_id):
    """Delete a tenant profile."""
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        click.echo("Tenant not found.")
        return
    
    db.session.delete(tenant)
    db.session.commit()
    click.echo(f"Tenant profile {tenant_id} has been deleted.")