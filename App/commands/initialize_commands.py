import click
from models import db
from app import app
from werkzeug.security import generate_password_hash

@app.cli.command("init-db")
@click.option('--default', is_flag=True, help="Initialize with default test data")
def init_db(default):
    """Initialize the database with optional default test data."""
    db.create_all()
    
    if default:
        # Import models here to avoid circular imports
        from models import User, Landlord, Tenant, Apartment, Amenity, ApartmentAmenity
        
        # Create default admin user
        admin = User(
            username="admin",
            email="admin@rentwise.com",
            password=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(admin)
        
        # Create default landlord
        landlord_user = User(
            username="landlord",
            email="landlord@rentwise.com",
            password=generate_password_hash("landlord123")
        )
        db.session.add(landlord_user)
        db.session.flush()
        
        landlord = Landlord(
            user_id=landlord_user.id,
            phone="555-0100"
        )
        db.session.add(landlord)
        db.session.flush()
        
        # Create default tenant
        tenant_user = User(
            username="tenant",
            email="tenant@rentwise.com",
            password=generate_password_hash("tenant123")
        )
        db.session.add(tenant_user)
        db.session.flush()
        
        tenant = Tenant(
            user_id=tenant_user.id,
            phone="678-0200"
        )
        db.session.add(tenant)
        
        # Create default amenities
        amenities = [
            Amenity(name="Parking", description="Reserved parking spot"),
            Amenity(name="Pool", description="Access to swimming pool"),
            Amenity(name="Gym", description="24/7 fitness center access"),
            Amenity(name="WiFi", description="High-speed internet included"),
            Amenity(name="Security", description="24/7 security system")
        ]
        for amenity in amenities:
            db.session.add(amenity)
        db.session.flush()
        
        # Create default apartments
        apartments = [
            Apartment(
                address="123 Main St",
                rent=1200.00,
                landlord_id=landlord.id,
                description="Modern 2-bedroom apartment"
            ),
            Apartment(
                address="456 Oak Ave",
                rent=950.00,
                landlord_id=landlord.id,
                description="Cozy 1-bedroom apartment"
            )
        ]
        for apartment in apartments:
            db.session.add(apartment)
        db.session.flush()
        
        # Add amenities to apartments
        apartment_amenities = [
            ApartmentAmenity(apartment_id=apartments[0].id, amenity_id=amenities[0].id),
            ApartmentAmenity(apartment_id=apartments[0].id, amenity_id=amenities[1].id),
            ApartmentAmenity(apartment_id=apartments[0].id, amenity_id=amenities[3].id),
            ApartmentAmenity(apartment_id=apartments[1].id, amenity_id=amenities[0].id),
            ApartmentAmenity(apartment_id=apartments[1].id, amenity_id=amenities[4].id)
        ]
        for apt_amenity in apartment_amenities:
            db.session.add(apt_amenity)
        
        db.session.commit()
        click.echo("Database initialized with default test data.")
    else:
        click.echo("Database initialized successfully.")

@app.cli.command("reset-db")
@click.option('--default', is_flag=True, help="Reset and initialize with default test data")
@click.confirmation_option(prompt="Are you sure you want to reset the database?")
def reset_db(default):
    """Reset the database and optionally add default test data (WARNING: This will delete all data)."""
    db.drop_all()
    db.create_all()
      
    if default:
        init_db(default=True)
    else:
        click.echo("Database has been reset successfully.")