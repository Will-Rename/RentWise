import click
from models import db, User
from app import app

@app.cli.command("create-user")
@click.option('--default', is_flag=True, help="Create a default test user")
@click.option('--username', prompt=True, help="User's username")
@click.option('--email', prompt=True, help="User's email address")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="User's password")
def create_user(default, username, email, password):
    """Creates a new user: prompted OR default test user."""
    if default:
        username = "testuser"
        email = "test@example.com"
        password = "testpass"
        click.echo("Creating default test user...")
    
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"User '{username}' created successfully.")

@app.cli.command("list-users")
def list_users():
    """List all registered users."""
    users = User.query.all()
    if not users:
        click.echo("No users found.")
        return
    
    for user in users:
        click.echo(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")