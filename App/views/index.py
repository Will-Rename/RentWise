from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for

from App.models import User, Tenant, Landlord, Apartment, Amenity, ApartmentAmenity, Review

from App.models import db

from App.controllers import create_user, initialize

from flask_jwt_extended import get_jwt_identity, jwt_required, current_user, unset_jwt_cookies, set_access_cookies

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})


@index_views.route('/search', methods=['POST'])
def search_from_index():
    query = request.form.get('query')

    if not query:
        return render_template('index.html', results=[], message="Please enter a search term.")

    results = Apartment.query.filter(
        Apartment.name.ilike(f'%{query}%') |
        Apartment.location.ilike(f'%{query}%') |
        Apartment.description.ilike(f'%{query}%') |
        Apartment.amenities.ilike(f'%{query}%')
    ).all()

    count = len(results)

    return render_template('index.html', results=results, query=query, count=count)


#----------------------------------#

@index_views.route('/apartments/search')
def mock_search():
    # Check if already created
    existing_apartment = Apartment.query.filter_by(apartment_name="Sunshine").first()
    if not existing_apartment:
        # Create landlord
        landlord_user = User(name="jane", email="jane@example.com", password="pass123")
        landlord = Landlord(name="jane", email="jane@example.com", password="pass123", phone_number="123-456-7890")
        landlord.user = landlord_user
        db.session.add(landlord_user)
        db.session.add(landlord)

        # Create apartment
        apartment = Apartment(
            apartment_name="Sunshine",
            apartment_location="Kingston",
            number_of_units_available=5,
            number_of_units_not_available=2,
            apartment_details="Cozy 2-bedroom with ocean view",
            landlord=landlord
        )
        db.session.add(apartment)

        # Create amenities
        washer = Amenity(amenity_name="Washer")
        tv = Amenity(amenity_name="TV")
        db.session.add_all([washer, tv])
        db.session.commit()

        db.session.add_all([
            ApartmentAmenity(apartment_id=apartment.apartment_id, amenity_id=washer.amenity_id, quantity=1),
            ApartmentAmenity(apartment_id=apartment.apartment_id, amenity_id=tv.amenity_id, quantity=2)
        ])

        # Create tenant
        tenant_user = User(name="bob", email="bob@example.com", password="tenantpass")
        tenant = Tenant(name="bob", email="bob@example.com", password="tenantpass", apartment_id=apartment.apartment_id)
        tenant.user = tenant_user
        db.session.add_all([tenant_user, tenant])

        # Create review
        review = Review(apartment_id=apartment.apartment_id, tenant_id=tenant.id, review_text="Love the view and the amenities!")
        db.session.add(review)

        db.session.commit()

    # Retrieve all apartments
    apartments = Apartment.query.all()
    return render_template('message.html', apartments=apartments)