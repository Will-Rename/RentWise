from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for

from App.models import User, Tenant, Landlord, Apartment, Amenity, ApartmentAmenity, Review

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
@jwt_required()
def search_from_index():
    query = request.form.get('query')

    # You can use current_user here if you're using a user_loader callback
    username = current_user.name

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