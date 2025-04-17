import click
from models import db, Tenant
from app import app

@app.cli.command("create-tenant")
@click.option('--user-id', type=int, prompt=True, help="Associated user ID")
@click.option('--phone', prompt=True, help="Contact phone number")
def create_tenant(user_id, phone):
    """Creates a new tenant profile."""
    tenant = Tenant(user_id=user_id, phone=phone)
    db.session.add(tenant)
    db.session.commit()
    click.echo(f"Tenant profile created for user ID {user_id}")

@app.cli.command("list-tenants")
def list_tenants():
    """List all tenants."""
    tenants = Tenant.query.all()
    if not tenants:
        click.echo("No tenants found.")
        return
    for tenant in tenants:
        click.echo(f"ID: {tenant.id}, User ID: {tenant.user_id}, Phone: {tenant.phone}")