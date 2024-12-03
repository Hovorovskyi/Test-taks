from app.models import User, db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from functools import wraps


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'viewer')

    if role not in ['admin', 'editor', 'viewer']:
        return jsonify({'message': 'Invalid role'}), 400

    if not username or not email or not password:
        return jsonify({'message': 'Missing request fields'}), 400

    if "@" not in email or "." not in email:
        return jsonify({'message': 'Invalid email address'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already in use'}), 400

    try:
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity={'id': user.id, 'email': user.email},
                                           additional_claims={"sub": str(user.id), "role": user.role})
        refresh_token = create_refresh_token(identity={'id': user.id, 'email': user.email},
                                             additional_claims={"sub": str(user.id), "role": user.role})

        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating user: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity={'id': user.id, 'email': user.email},
                                       additional_claims={"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token(identity={'id': user.id, 'email': user.email},
                                         additional_claims={"sub": str(user.id), "role": user.role})

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_access_token}), 200


def role_required(required_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                claims = get_jwt()
                user_role = claims.get('role')
                if user_role not in required_roles:
                    return jsonify({'message': 'You don`t have access to this resource'}), 403
            except Exception as e:
                return jsonify({'message': f'Error in role_required: {str(e)}'}), 500
            return fn(*args, **kwargs)
        return decorator
    return wrapper
