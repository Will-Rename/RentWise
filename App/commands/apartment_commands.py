import click
from models import db, Apartment
from app import app

@app.cli.command("create-apartment")
@click.option('--address', prompt=True, help="Apartment address")
@click.option('--rent', type=float, prompt=True, help="Monthly rent")
@click.option('--landlord-id', type=int, prompt=True, help="Landlord ID")
def create_apartment(address, rent, landlord_id):
    """Creates a new apartment listing."""
    apartment = Apartment(address=address, rent=rent, landlord_id=landlord_id)
    db.session.add(apartment)
    db.session.commit()
    click.echo(f"Apartment at '{address}' created successfully.")

@app.cli.command("list-apartments")
def list_apartments():
    """List all apartments."""
    apartments = Apartment.query.all()
    if not apartments:
        click.echo("No apartments found.")
        return
    for apt in apartments:
        click.echo(f"ID: {apt.id}, Address: {apt.address}, Rent: ${apt.rent}")