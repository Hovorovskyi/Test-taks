from app.models import User, db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .auth import role_required


user_bp = Blueprint('users', __name__)


@user_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_users():
    users = User.query.all()
    result = [{'id': u.id, 'username': u.username, 'email': u.email, 'role': u.role} for u in users]
    return jsonify(result), 200


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role.value}), 200


@user_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_user():
    data = request.get_json()
    if not data or "username" not in data or "email" not in data or "password" not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password'],
        role=data.get('role', 'viewer')
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created', 'user_id': new_user.id}), 201


@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password_hash = data['password']
    if 'role' in data:
        user.role = data['role']

    db.session.commit()

    return jsonify({'message': 'User updated'}), 200


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted'}), 200


@user_bp.route('/search', methods=['GET'])
@jwt_required()
@role_required(['admin', 'editor'])
def search_users():
    query = request.args.get('q')
    if not query:
        return jsonify({'message': "Missing search parameter 'q'"}), 400

    users = User.query.filter(
        (User.username.ilike(f"%{query}%")) |
        (User.email.ilike(f"%{query}%"))
    ).all()

    result = [
        {'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}
        for user in users
    ]
    return jsonify(result), 200

