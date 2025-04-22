from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from App.models import Review, Apartment
from App.database import db
from App.controllers import (
    create_review,
    delete_tenant_review,
    get_apartment_reviews,
    get_tenant_reviews
)

reviews_views = Blueprint('reviews_views', __name__, template_folder='../templates')

@reviews_views.route('/apartments/<int:apartment_id>/reviews')
def apartment_reviews_page(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    reviews = get_apartment_reviews(apartment_id)
    return render_template('reviews.html', 
                         apartment=apartment,
                         reviews=reviews)

@reviews_views.route('/api/reviews/<int:apartment_id>', methods=['POST'])
@jwt_required()
def create_review_api(apartment_id):
    if current_user.type != 'tenant':
        return jsonify({'error': 'Only tenants can create reviews'}), 403
    
    data = request.json
    review = create_review(current_user.user_id, apartment_id, data['review_text'])
    
    if review:
        return jsonify({'message': 'Review created successfully'}), 201
    return jsonify({'error': 'Failed to create review'}), 400

@reviews_views.route('/api/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review_api(review_id):
    review = Review.query.get_or_404(review_id)
    
    if current_user.user_id != review.tenant_id:
        return jsonify({'error': 'Not authorized'}), 403
    
    data = request.json
    review.review_text = data['review_text']
    db.session.commit()
    
    return jsonify({'message': 'Review updated successfully'})

@reviews_views.route('/api/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review_api(review_id):
    result = delete_tenant_review(current_user.user_id, review_id)
    if result:
        return jsonify({'message': 'Review deleted successfully'})
    return jsonify({'error': 'Failed to delete review'}), 400