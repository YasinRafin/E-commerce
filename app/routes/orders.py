from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Order, OrderItem, CartItem, Product, OrderStatus
from sqlalchemy.exc import IntegrityError

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    if not data.get('shipping_address'):
        return jsonify({'error': 'Shipping address is required'}), 400

    try:
        total_amount = 0
        order_items = []

        for cart_item in cart_items:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                return jsonify({
                    'error': f'Not enough stock for product: {product.name}'
                }), 400

            total_amount += product.price * cart_item.quantity
            order_items.append({
                'product': product,
                'quantity': cart_item.quantity,
                'price': product.price
            })

        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status=OrderStatus.PENDING.value,
            shipping_address=data['shipping_address']
        )
        db.session.add(order)
        db.session.flush()

        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            item['product'].stock -= item['quantity']
            db.session.add(order_item)

        for cart_item in cart_items:
            db.session.delete(cart_item)

        db.session.commit()

        return jsonify({
            'order_id': order.id,
            'total_amount': order.total_amount,
            'status': order.status
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order'}), 500


@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    return jsonify({
        'orders': [{
            'id': order.id,
            'total_amount': order.total_amount,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'tracking_number': order.tracking_number,
            'items': [{
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': item.price,
                'subtotal': item.quantity * item.price
            } for item in order.items]
        } for order in orders]
    })


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()

    return jsonify({
        'id': order.id,
        'total_amount': order.total_amount,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'updated_at': order.updated_at.isoformat(),
        'shipping_address': order.shipping_address,
        'tracking_number': order.tracking_number,
        'items': [{
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.price,
            'subtotal': item.quantity * item.price
        } for item in order.items]
    })


@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()

    if order.status != OrderStatus.PENDING.value:
        return jsonify({'error': 'Only pending orders can be cancelled'}), 400

    try:
        for item in order.items:
            item.product.stock += item.quantity

        order.status = OrderStatus.CANCELLED.value
        db.session.commit()

        return jsonify({
            'message': 'Order cancelled successfully',
            'order_id': order.id
        })

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel order'}), 500
