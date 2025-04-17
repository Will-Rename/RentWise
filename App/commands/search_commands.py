import click
from models import db, Apartment, Amenity, ApartmentAmenity
from app import app

@app.cli.command("search-apartments")
@click.option('--location', help="Search by location")
@click.option('--amenity', help="Search by amenity name")
def search_apartments(location, amenity):
    """Search for apartments by location and/or amenity."""
    if not location and not amenity:
        click.echo("Please provide either location or amenity to search.")
        return

    found = []
    
    if location and not amenity:
        click.echo(f"Searching for apartments in location: {location}")
        found = Apartment.query.filter_by(apartment_location=location).all()

    elif amenity and not location:
        click.echo(f"Searching for apartments with amenity: {amenity}")
        amenity_found = Amenity.query.filter_by(amenity_name=amenity).first()
        
        if not amenity_found:
            click.echo(f"Amenity '{amenity}' not found.")
            return

        amenity_found_apartments = ApartmentAmenity.query.filter_by(amenity_id=amenity_found.id).all()
        found = [apt_amenity.apartment for apt_amenity in amenity_found_apartments if apt_amenity.apartment]

    elif location and amenity:
        click.echo(f"Searching for apartments in {location} with amenity: {amenity}")
        amenity_found = Amenity.query.filter_by(amenity_name=amenity).first()
        
        if not amenity_found:
            click.echo(f"Amenity '{amenity}' not found.")
            return

        found = Apartment.query.join(ApartmentAmenity).filter(
            Apartment.apartment_location == location,
            ApartmentAmenity.amenity_id == amenity_found.id
        ).all()

    if not found:
        click.echo("No apartments found matching your criteria.")
        return

    click.echo("\nFound apartments:")
    for apartment in found:
        click.echo(f"\nID: {apartment.id}")
        click.echo(f"Name: {apartment.apartment_name}")
        click.echo(f"Location: {apartment.apartment_location}")
        click.echo(f"Available Units: {apartment.number_of_units_available}")
        click.echo(f"Details: {apartment.apartment_details}")
        click.echo("-" * 40)

@app.cli.command("list-all-apartments")
def list_all_apartments():
    """List all apartments in the system."""
    apartments = Apartment.query.all()
    
    if not apartments:
        click.echo("No apartments found in the system.")
        return
    
    click.echo("\nAll apartments:")
    for apartment in apartments:
        click.echo(f"\nID: {apartment.id}")
        click.echo(f"Name: {apartment.apartment_name}")
        click.echo(f"Location: {apartment.apartment_location}")
        click.echo(f"Available Units: {apartment.number_of_units_available}")
        click.echo(f"Not Available Units: {apartment.number_of_units_not_available}")
        click.echo(f"Details: {apartment.apartment_details}")
        
        # List amenities for this apartment
        amenities = db.session.query(Amenity).\
            join(ApartmentAmenity).\
            filter(ApartmentAmenity.apartment_id == apartment.id).\
            all()
        
        if amenities:
            click.echo("Amenities:")
            for amenity in amenities:
                click.echo(f"  - {amenity.amenity_name}")
        
        click.echo("-" * 40)