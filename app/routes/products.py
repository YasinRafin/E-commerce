from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, Product, Category
from ..utils.pagination import paginate
from sqlalchemy.exc import IntegrityError

products_bp = Blueprint('products', __name__)


@products_bp.route('', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock = request.args.get('in_stock', type=bool)

    query = Product.query

    if category_id:
        query = query.filter_by(category_id=category_id)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if in_stock:
        query = query.filter(Product.stock > 0)

    return paginate(query, page, per_page)


@products_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()

    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock'],
        category_id=data['category_id']
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category_id': product.category_id
    }), 201


@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    try:
        if 'name' in data:
            if not data['name'].strip():
                return jsonify({'error': 'Name cannot be empty'}), 400
            product.name = data['name']

        if 'description' in data:
            product.description = data.get('description', '')

        if 'price' in data:
            if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
                return jsonify({'error': 'Price must be a positive number'}), 400
            product.price = data['price']

        if 'stock' in data:
            if not isinstance(data['stock'], int) or data['stock'] < 0:
                return jsonify({'error': 'Stock must be a non-negative integer'}), 400
            product.stock = data['stock']

        if 'category_id' in data:
            if not Category.query.get(data['category_id']):
                return jsonify({'error': 'Invalid category ID'}), 400
            product.category_id = data['category_id']

        db.session.commit()

        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'category_id': product.category_id,
            'category_name': product.category.name
        })

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to update product'}), 500


@products_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})
