import click
from models import db, User
from app import app
from werkzeug.security import generate_password_hash

@app.cli.command("create-user")
@click.option('--default', is_flag=True, help="Create a default test user")
@click.option('--username', prompt=True, help="User's username")
@click.option('--email', prompt=True, help="User's email address")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="User's password")
def create_user(default, username, email, password):
    """Creates a new user: prompted OR default test user."""
    if default:
        username = "testuser"
        email = "test@rentwise.com"
        password = "test123"
        click.echo("Creating default test user...")
    
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
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
        role = "Admin" if user.is_admin else "Regular"
        status = "Active" if user.is_active else "Inactive"
        click.echo(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {role}, Status: {status}")

@app.cli.command("delete-user")
@click.option('--email', prompt=True, help="User's email address")
@click.confirmation_option(prompt="Are you sure you want to delete this user?")
def delete_user(email):
    """Delete a user account."""
    user = User.query.filter_by(email=email).first()
    if not user:
        click.echo("User not found.")
        return
    
    db.session.delete(user)
    db.session.commit()
    click.echo(f"User '{user.username}' has been deleted.")