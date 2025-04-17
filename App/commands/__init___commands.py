import click
from models import db
from app import app

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    click.echo("Database initialized successfully.")

@app.cli.command("reset-db")
@click.confirmation_option(prompt="Are you sure you want to reset the database?")
def reset_db():
    """Reset the database (WARNING: This will delete all data)."""
    db.drop_all()
    db.create_all()
    click.echo("Database has been reset successfully.")