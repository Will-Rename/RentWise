import click
from models import db, Tenant, User, Review
from app import app
from werkzeug.security import generate_password_hash

@app.cli.command("create-tenant")
@click.option('--default', is_flag=True, help="Create a default tenant profile")
@click.option('--user-id', type=int, prompt=True, help="Associated user ID")
@click.option('--phone', prompt=True, help="Contact phone number")
def create_tenant(default, user_id, phone):
    """Creates a new tenant profile."""
    if default:  
        # Create a default user first
        default_user = User(
            username="tenant",
            email="tenant@rentwise.com",
            password=generate_password_hash("tenant123")
        )
        db.session.add(default_user)
        db.session.flush()
        user_id = default_user.id
        phone = "555-0200"
        click.echo("Creating default tenant profile...")

    tenant = Tenant(user_id=user_id, phone=phone)
    db.session.add(tenant)
    db.session.commit()
    click.echo(f"Tenant profile created for user ID {user_id}")

@app.cli.command("list-tenants")
def list_tenants():
    """List all tenants."""
    tenants = Tenant.query.join(User).all()
    if not tenants:
        click.echo("No tenants found.")
        return
    
    for tenant in tenants:
        click.echo(f"ID: {tenant.id}, User: {tenant.user.username}, Phone: {tenant.phone}")

@app.cli.command("update-tenant-phone")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
@click.option('--phone', prompt=True, help="New phone number")
def update_tenant_phone(tenant_id, phone):
    """Update a tenant's phone number."""
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        click.echo("Tenant not found.")
        return
    
    tenant.phone = phone
    db.session.commit()
    click.echo(f"Phone number updated for tenant ID {tenant_id}")

@app.cli.command("delete-tenant")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
@click.confirmation_option(prompt="Are you sure you want to delete this tenant?")
def delete_tenant(tenant_id):
    """Delete a tenant profile."""
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        click.echo("Tenant not found.")
        return
    
    db.session.delete(tenant)
    db.session.commit()
    click.echo(f"Tenant profile {tenant_id} has been deleted.")

@app.cli.command("create-review")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--review-text', prompt=True, help="Review text")
def create_review(tenant_id, apartment_id, review_text):
    """Create a review for an apartment."""
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        click.echo("Tenant not found.")
        return

    review = Review(
        tenant_id=tenant_id,
        apartment_id=apartment_id,
        review_text=review_text
    )
    db.session.add(review)
    db.session.commit()
    click.echo("Review created successfully.")

@app.cli.command("list-tenant-reviews")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
def list_tenant_reviews(tenant_id):
    """List all reviews by a tenant."""
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        click.echo("Tenant not found.")
        return
    
    reviews = Review.query.filter_by(tenant_id=tenant_id).all()
    if not reviews:
        click.echo("No reviews found for this tenant.")
        return

    for review in reviews:
        click.echo(f"\nReview ID: {review.id}")
        click.echo(f"Apartment ID: {review.apartment_id}")
        click.echo(f"Review: {review.review_text}")
        click.echo("---")

@app.cli.command("delete-review")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
@click.option('--review-id', type=int, prompt=True, help="Review ID")
@click.confirmation_option(prompt="Are you sure you want to delete this review?")
def delete_review(tenant_id, review_id):
    """Delete a tenant's review."""
    review = Review.query.get(review_id)
    if not review:
        click.echo("Review not found.")
        return
    
    if review.tenant_id != tenant_id:
        click.echo("Not authorized to delete this review.")
        return
    
    db.session.delete(review)
    db.session.commit()
    click.echo("Review deleted successfully.")