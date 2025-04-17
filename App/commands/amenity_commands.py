import click
from models import db, Amenity
from app import app

@app.cli.command("create-amenity")
@click.option('--default', is_flag=True, help="Create default amenities")
@click.option('--name', prompt=True, help="Amenity name")
@click.option('--description', prompt=True, help="Amenity description")
def create_amenity(default, name, description):
    """Creates a new amenity or default amenities."""
    if default:
        default_amenities = [
            ("Parking", "Reserved parking spot"),
            ("Pool", "Access to swimming pool"),
            ("Gym", "24/7 fitness center access"),
            ("WiFi", "High-speed internet included"),
            ("Security", "24/7 security system")
        ]
        for amenity_name, amenity_desc in default_amenities:
            amenity = Amenity(name=amenity_name, description=amenity_desc)
            db.session.add(amenity)
        db.session.commit()
        click.echo("Default amenities created successfully.")
        return

    amenity = Amenity(name=name, description=description)
    db.session.add(amenity)
    db.session.commit()
    click.echo(f"Amenity '{name}' created successfully.")

@app.cli.command("list-amenities")
def list_amenities():
    """List all amenities."""
    amenities = Amenity.query.all()
    if not amenities:
        click.echo("No amenities found.")
        return
    
    for amenity in amenities:
        click.echo(f"ID: {amenity.id}, Name: {amenity.name}")
        click.echo(f"Description: {amenity.description}")
        click.echo("---")

@app.cli.command("update-amenity")
@click.option('--amenity-id', type=int, prompt=True, help="Amenity ID")
@click.option('--name', prompt=True, help="New amenity name")
@click.option('--description', prompt=True, help="New amenity description")
def update_amenity(amenity_id, name, description):
    """Update an amenity's details."""
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        click.echo("Amenity not found.")
        return
    
    amenity.name = name
    amenity.description = description
    db.session.commit()
    click.echo(f"Amenity {amenity_id} updated successfully.")

@app.cli.command("delete-amenity")
@click.option('--amenity-id', type=int, prompt=True, help="Amenity ID")
@click.confirmation_option(prompt="Are you sure you want to delete this amenity?")
def delete_amenity(amenity_id):
    """Delete an amenity."""
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        click.echo("Amenity not found.")
        return
    
    name = amenity.name
    db.session.delete(amenity)
    db.session.commit()
    click.echo(f"Amenity '{name}' has been deleted.")