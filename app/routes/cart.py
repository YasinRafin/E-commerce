from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, CartItem, Product, User
from sqlalchemy.exc import IntegrityError

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    total = subtotal

    return jsonify({
        'items': [{
            'id': item.id,
            'product_id': item.product_id,
            'product_name': item.product.name,
            'product_description': item.product.description,
            'quantity': item.quantity,
            'unit_price': item.product.price,
            'subtotal': item.product.price * item.quantity,
            'stock_available': item.product.stock
        } for item in cart_items],
        'summary': {
            'subtotal': subtotal,
            'total': total,
            'item_count': sum(item.quantity for item in cart_items)
        }
    })


@cart_bp.route('', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data.get('product_id'):
        return jsonify({'error': 'Product ID is required'}), 400

    quantity = data.get('quantity', 1)
    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({'error': 'Quantity must be a positive integer'}), 400

    product = Product.query.get_or_404(data['product_id'])
    if product.stock < quantity:
        return jsonify({
            'error': 'Not enough stock',
            'available': product.stock
        }), 400

    try:
        cart_item = CartItem.query.filter_by(
            user_id=user_id,
            product_id=data['product_id']
        ).first()

        if cart_item:
            if product.stock < (cart_item.quantity + quantity):
                return jsonify({
                    'error': 'Not enough stock',
                    'available': product.stock,
                    'in_cart': cart_item.quantity
                }), 400

            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=data['product_id'],
                quantity=quantity
            )
            db.session.add(cart_item)

        db.session.commit()

        return jsonify({
            'message': 'Item added to cart',
            'cart_item': {
                'id': cart_item.id,
                'product_id': cart_item.product_id,
                'product_name': cart_item.product.name,
                'quantity': cart_item.quantity,
                'unit_price': cart_item.product.price,
                'subtotal': cart_item.product.price * cart_item.quantity
            }
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to add item to cart'}), 500


@cart_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    if 'quantity' not in data:
        return jsonify({'error': 'Quantity is required'}), 400
    if not isinstance(data['quantity'], int) or data['quantity'] < 0:
        return jsonify({'error': 'Quantity must be a non-negative integer'}), 400

    cart_item = CartItem.query.filter_by(
        id=item_id,
        user_id=user_id
    ).first_or_404()

    try:
        if data['quantity'] == 0:
            db.session.delete(cart_item)
        else:
            if cart_item.product.stock < data['quantity']:
                return jsonify({
                    'error': 'Not enough stock',
                    'available': cart_item.product.stock
                }), 400

            cart_item.quantity = data['quantity']

        db.session.commit()

        return jsonify({
            'message': 'Cart updated successfully'
        })

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to update cart'}), 500


@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(
        id=item_id,
        user_id=user_id
    ).first_or_404()

    try:
        db.session.delete(cart_item)
        db.session.commit()

        return jsonify({
            'message': 'Item removed from cart'
        })

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove item from cart'}), 500
