import click
from models import db, Landlord
from app import app

@app.cli.command("create-landlord")
@click.option('--user-id', type=int, prompt=True, help="Associated user ID")
@click.option('--phone', prompt=True, help="Contact phone number")
def create_landlord(user_id, phone):
    """Creates a new landlord profile."""
    landlord = Landlord(user_id=user_id, phone=phone)
    db.session.add(landlord)
    db.session.commit()
    click.echo(f"Landlord profile created for user ID {user_id}")

@app.cli.command("list-landlords")
def list_landlords():
    """List all landlords."""
    landlords = Landlord.query.all()
    if not landlords:
        click.echo("No landlords found.")
        return
    for landlord in landlords:
        click.echo(f"ID: {landlord.id}, User ID: {landlord.user_id}, Phone: {landlord.phone}")