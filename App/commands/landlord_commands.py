import click
from models import db, Landlord, User
from app import app
from werkzeug.security import generate_password_hash

@app.cli.command("create-landlord")
@click.option('--default', is_flag=True, help="Create a default landlord profile")
@click.option('--user-id', type=int, prompt=True, help="Associated user ID")
@click.option('--phone', prompt=True, help="Contact phone number")
def create_landlord(default, user_id, phone):
    """Creates a new landlord profile."""
    if default:
        # Create a default user first
        default_user = User(
            username="landlord",
            email="landlord@rentwise.com",
            password=generate_password_hash("landlord123")
        )
        db.session.add(default_user)
        db.session.flush()
        user_id = default_user.id
        phone = "555-0100"
        click.echo("Creating default landlord profile...")

    landlord = Landlord(user_id=user_id, phone=phone)
    db.session.add(landlord)
    db.session.commit()
    click.echo(f"Landlord profile created for user ID {user_id}")

@app.cli.command("list-landlords")
def list_landlords():
    """List all landlords."""
    landlords = Landlord.query.join(User).all()
    if not landlords:
        click.echo("No landlords found.")
        return
    
    for landlord in landlords:
        click.echo(f"ID: {landlord.id}, User: {landlord.user.username}, Phone: {landlord.phone}")

@app.cli.command("update-landlord-phone")
@click.option('--landlord-id', type=int, prompt=True, help="Landlord ID")
@click.option('--phone', prompt=True, help="New phone number")
def update_landlord_phone(landlord_id, phone):
    """Update a landlord's phone number."""
    landlord = Landlord.query.get(landlord_id)
    if not landlord:
        click.echo("Landlord not found.")
        return
    
    landlord.phone = phone
    db.session.commit()
    click.echo(f"Phone number updated for landlord ID {landlord_id}")