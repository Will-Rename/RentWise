import click
from models import db, User
from app import app
from flask_login import login_user
from werkzeug.security import generate_password_hash

@app.cli.command("create-admin")
@click.option('--default', is_flag=True, help="Create a default admin user")
@click.option('--username', prompt=True, help="Admin username")
@click.option('--email', prompt=True, help="Admin email")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="Admin password")
def create_admin(default, username, email, password):
    """Creates a new admin user."""
    if default:
        username = "admin"
        email = "admin@rentwise.com"
        password = "admin123"
        click.echo("Creating default admin user...")

    hashed_password = generate_password_hash(password)
    admin = User(username=username, email=email, password=hashed_password, is_admin=True)
    db.session.add(admin)
    db.session.commit()
    click.echo(f"Admin user '{username}' created successfully.")

@app.cli.command("reset-password")
@click.option('--default', is_flag=True, help="Reset password to default value")
@click.option('--email', prompt=True, help="User's email address")
@click.option('--new-password', prompt=True, hide_input=True, confirmation_prompt=True, help="New password")
def reset_password(default, email, new_password):
    """Reset a user's password."""
    user = User.query.filter_by(email=email).first()
    if not user:
        click.echo("User not found.")
        return
    
    if default:
        if user.is_admin:
            new_password = "admin123"
        elif hasattr(user, 'landlord'):
            new_password = "landlord123"
        else:
            new_password = "tenant123"
        click.echo(f"Resetting to default password for {user.username}...")

    user.password = generate_password_hash(new_password)
    db.session.commit()
    click.echo(f"Password reset successfully for user: {user.username}")

@app.cli.command("list-admins")
def list_admins():
    """List all admin users."""
    admins = User.query.filter_by(is_admin=True).all()
    if not admins:
        click.echo("No admin users found.")
        return
    
    for admin in admins:
        click.echo(f"ID: {admin.id}, Username: {admin.username}, Email: {admin.email}")

@app.cli.command("deactivate-user")
@click.option('--email', prompt=True, help="User's email address")
@click.confirmation_option(prompt="Are you sure you want to deactivate this user?")
def deactivate_user(email):
    """Deactivate a user account."""
    user = User.query.filter_by(email=email).first()
    if not user:
        click.echo("User not found.")
        return
    
    user.is_active = False
    db.session.commit()
    click.echo(f"User '{user.username}' has been deactivated.")