from flask import jsonify


def paginate(query, page, per_page):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [{
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'stock': item.stock,
            'category_id': item.category_id
        } for item in pagination.items],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })
