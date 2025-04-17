import click
from models import db, ApartmentAmenity, Apartment, Amenity
from app import app

@app.cli.command("add-apartment-amenity")
@click.option('--default', is_flag=True, help="Add default amenities to an apartment")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--amenity-id', type=int, help="Amenity ID")
def add_apartment_amenity(default, apartment_id, amenity_id):
    """Links an amenity to an apartment."""
    apartment = Apartment.query.get(apartment_id)
    if not apartment:
        click.echo("Apartment not found.")
        return  

    if default:
        # Add a standard set of amenities (first 3 available amenities)
        amenities = Amenity.query.limit(3).all()
        if not amenities:
            click.echo("No amenities found to add. Please create some amenities first.")
            return
        
        for amenity in amenities:
            existing = ApartmentAmenity.query.filter_by(
                apartment_id=apartment_id,
                amenity_id=amenity.id
            ).first()
            
            if not existing:
                apartment_amenity = ApartmentAmenity(
                    apartment_id=apartment_id,
                    amenity_id=amenity.id
                )
                db.session.add(apartment_amenity)
                click.echo(f"Added amenity '{amenity.name}' to apartment {apartment_id}")
        
        db.session.commit()
        return

    if not amenity_id:
        click.echo("Amenity ID is required when not using default option.")
        return

    existing = ApartmentAmenity.query.filter_by(
        apartment_id=apartment_id,
        amenity_id=amenity_id
    ).first()
    
    if existing:
        click.echo("This amenity is already linked to the apartment.")
        return

    apartment_amenity = ApartmentAmenity(apartment_id=apartment_id, amenity_id=amenity_id)
    db.session.add(apartment_amenity)
    db.session.commit()
    click.echo(f"Added amenity {amenity_id} to apartment {apartment_id}")

@app.cli.command("list-apartment-amenities")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
def list_apartment_amenities(apartment_id):
    """List all amenities for a specific apartment."""
    apartment = Apartment.query.get(apartment_id)
    if not apartment:
        click.echo("Apartment not found.")
        return

    amenities = db.session.query(Amenity).\
        join(ApartmentAmenity).\
        filter(ApartmentAmenity.apartment_id == apartment_id).\
        all()

    if not amenities:
        click.echo(f"No amenities found for apartment {apartment_id}")
        return

    click.echo(f"Amenities for apartment at {apartment.address}:")
    for amenity in amenities:
        click.echo(f"- {amenity.name}: {amenity.description}")

@app.cli.command("remove-apartment-amenity")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--amenity-id', type=int, prompt=True, help="Amenity ID")
@click.confirmation_option(prompt="Are you sure you want to remove this amenity?")
def remove_apartment_amenity(apartment_id, amenity_id):
    """Remove an amenity from an apartment."""
    apartment_amenity = ApartmentAmenity.query.filter_by(
        apartment_id=apartment_id,
        amenity_id=amenity_id
    ).first()
    
    if not apartment_amenity:
        click.echo("This amenity is not linked to the apartment.")
        return

    amenity = Amenity.query.get(amenity_id)
    db.session.delete(apartment_amenity)
    db.session.commit()
    click.echo(f"Removed amenity '{amenity.name}' from apartment {apartment_id}")