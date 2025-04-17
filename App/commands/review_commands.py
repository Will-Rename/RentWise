import click
from models import db, Review, Tenant, Apartment
from app import app

@app.cli.command("create-review")
@click.option('--default', is_flag=True, help="Create a default review")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID")
@click.option('--apartment-id', type=int, prompt=True, help="Apartment ID")
@click.option('--review-text', prompt=True, help="Review text")
def create_review(default, tenant_id, apartment_id, review_text):
    """Creates a new review for an apartment."""
    if default:
        # Get the first tenant and apartment
        tenant = Tenant.query.first()
        apartment = Apartment.query.first()
        if not tenant or not apartment:
            click.echo("Error: Need at least one tenant and apartment in the system.")
            return
        tenant_id = tenant.id
        apartment_id = apartment.id
        review_text = "Great apartment with excellent amenities!"
        click.echo("Creating default review...")

    # Validate tenant and apartment
    tenant = Tenant.query.get(tenant_id)
    apartment = Apartment.query.get(apartment_id)
    
    if not tenant:
        click.echo("Tenant not found.")
        return
    
    if not apartment:
        click.echo("Apartment not found.")
        return

    review = Review(
        tenant_id=tenant_id,
        apartment_id=apartment_id,
        review_text=review_text
    )
    db.session.add(review)
    db.session.commit()
    click.echo(f"Review created successfully for apartment {apartment_id}")

@app.cli.command("list-reviews")
@click.option('--apartment-id', type=int, help="Filter by apartment ID")
@click.option('--tenant-id', type=int, help="Filter by tenant ID")
def list_reviews(apartment_id, tenant_id):
    """List reviews, optionally filtered by apartment or tenant."""
    query = Review.query
    
    if apartment_id:
        query = query.filter_by(apartment_id=apartment_id)
    if tenant_id:
        query = query.filter_by(tenant_id=tenant_id)
    
    reviews = query.all()
    if not reviews:
        click.echo("No reviews found.")
        return
    
    for review in reviews:
        click.echo(f"Review ID: {review.id}")
        click.echo(f"Apartment ID: {review.apartment_id}")
        click.echo(f"Tenant ID: {review.tenant_id}")
        click.echo(f"Review: {review.review_text}")
        click.echo("---")

@app.cli.command("delete-review")
@click.option('--review-id', type=int, prompt=True, help="Review ID")
@click.option('--tenant-id', type=int, prompt=True, help="Tenant ID (for verification)")
@click.confirmation_option(prompt="Are you sure you want to delete this review?")
def delete_review(review_id, tenant_id):
    """Delete a review (only by the tenant who created it)."""
    review = Review.query.get(review_id)
    if not review:
        click.echo("Review not found.")
        return
    
    if review.tenant_id != tenant_id:
        click.echo("Not authorized. Only the tenant who created the review can delete it.")
        return
    
    db.session.delete(review)
    db.session.commit()
    click.echo(f"Review {review_id} has been deleted.")