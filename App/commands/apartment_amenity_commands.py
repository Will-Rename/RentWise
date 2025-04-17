import click
from models import db, ApartmentAmenity, Apartment, Amenity
from app import app

@app.cli.command("add-apartment-amenity")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--amenity-id', type=int, prompt=True, help="Amenity ID")
def add_apartment_amenity(apartment_id, amenity_id):
    """Links an amenity to an apartment."""
    apartment_amenity = ApartmentAmenity(apartment_id=apartment_id, amenity_id=amenity_id)
    db.session.add(apartment_amenity)
    db.session.commit()
    click.echo(f"Added amenity {amenity_id} to apartment {apartment_id}")

@app.cli.command("list-apartment-amenities")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
def list_apartment_amenities(apartment_id):
    """List all amenities for a specific apartment."""
    amenities = ApartmentAmenity.query.filter_by(apartment_id=apartment_id).all()
    if not amenities:
        click.echo(f"No amenities found for apartment {apartment_id}")
        return
    for item in amenities:
        click.echo(f"Apartment ID: {item.apartment_id}, Amenity ID: {item.amenity_id}")