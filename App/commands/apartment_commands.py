import click
from models import db, Apartment, Landlord
from app import app

@app.cli.command("create-apartment")
@click.option('--default', is_flag=True, help="Create a default apartment")
@click.option('--address', prompt=True, help="Apartment address")
@click.option('--rent', type=float, prompt=True, help="Monthly rent")
@click.option('--landlord-id', type=int, prompt=True, help="Landlord ID")
@click.option('--description', prompt=True, help="Apartment description")
def create_apartment(default, address, rent, landlord_id, description):
    """Creates a new apartment listing."""
    if default:
        address = "123 Main St"
        rent = 1200.00
        # Get the first landlord in the system
        landlord = Landlord.query.first()
        if not landlord:
            click.echo("Error: No landlord found in the system. Create a landlord first.")
            return
        landlord_id = landlord.id
        description = "Modern 2-bedroom apartment"
        click.echo("Creating default apartment...")

    apartment = Apartment(
        address=address,
        rent=rent,
        landlord_id=landlord_id,
        description=description
    )
    db.session.add(apartment)
    db.session.commit()
    click.echo(f"Apartment at '{address}' created successfully.")

@app.cli.command("list-apartments")
@click.option('--landlord-id', type=int, help="Filter by landlord ID")
def list_apartments(landlord_id):

    """List all apartments, optionally filtered by landlord."""
    query = Apartment.query
    if landlord_id:
        query = query.filter_by(landlord_id=landlord_id)
    
    apartments = query.all()
    if not apartments:
        click.echo("No apartments found.")
        return
    
    for apt in apartments:
        click.echo(f"ID: {apt.id}, Address: {apt.address}, Rent: ${apt.rent:.2f}")
        click.echo(f"Description: {apt.description}")
        click.echo("---")

@app.cli.command("update-apartment-rent")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--new-rent', type=float, prompt=True, help="New monthly rent")
def update_apartment_rent(apartment_id, new_rent):
    """Update an apartment's monthly rent."""
    apartment = Apartment.query.get(apartment_id)
    if not apartment:
        click.echo("Apartment not found.")
        return
    
    old_rent = apartment.rent
    apartment.rent = new_rent
    db.session.commit()
    click.echo(f"Rent updated from ${old_rent:.2f} to ${new_rent:.2f}")

@app.cli.command("delete-apartment")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.confirmation_option(prompt="Are you sure you want to delete this apartment?")
def delete_apartment(apartment_id):
    """Delete an apartment listing."""
    apartment = Apartment.query.get(apartment_id)
    if not apartment:
        click.echo("Apartment not found.")
        return
    
    address = apartment.address
    db.session.delete(apartment)
    db.session.commit()
    click.echo(f"Apartment at '{address}' has been deleted.")