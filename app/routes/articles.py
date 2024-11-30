from app.models import Article, User, db
from .auth import role_required
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


article_bp = Blueprint('articles', __name__)


@article_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['editor', 'admin', 'viewer'])
def create_article():
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'message': 'Missing required fields: title and content'}), 400

        title = data.get('title')
        content = data.get('content')

        if not isinstance(title, str) or not isinstance(content, str):
            return jsonify({'message': 'Title and content must be strings'}), 422

        if not title.strip() or not content.strip():
            return jsonify({'message': 'Title and content cannot be empty'}), 422

        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        article = Article(title=title, content=content, author_id=current_user_id)
        db.session.add(article)
        db.session.commit()

        return jsonify({'message': 'Article created successfully'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@article_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin', 'editor', 'viewer'])
def get_articles():
    articles = Article.query.all()
    result = ([
        {
            'id': a.id,
            'title': a.title,
            'content': a.content,
            'author_id': a.author_id,
            'author_username': a.author.username
        }
        for a in articles]
    )
    return jsonify(result), 200


@article_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'editor', 'viewer'])
def get_one_article(id):
    article = db.session.get(Article, id)
    if not article:
        jsonify({'message': 'Article not found'}), 404

    result = {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author_id': article.author_id,
            'author_username': article.author.username
    }
    return jsonify(result), 200


@article_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_article(id):
    current_user_id = get_jwt_identity()

    claims = get_jwt()
    current_user_role = claims.get("role")

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    article = db.session.get(Article, id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404

    if current_user_role not in ['admin', 'editor'] and article.author_id != int(current_user_id):
        return jsonify({'message': 'Access forbidden: you are not allowed to edit this article'}), 403

    if 'title' in data:
        article.title = data['title']
    if 'content' in data:
        article.content = data['content']

    db.session.commit()
    return jsonify({'message': 'Article updated successfully'}), 200


@article_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_article(id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    current_user_role = claims.get("role")

    article = db.session.get(Article, id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404

    if current_user_role != 'admin' and article.author_id != int(current_user_id):
        return jsonify({'message': 'Access forbidden: you are not allowed to delete this article'}), 403

    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': 'Article deleted successfully'}), 200


@article_bp.route('/search', methods=['GET'])
@jwt_required()
def search_articles():
    query = request.args.get('q')
    if not query:
        return jsonify({'message': "Missing search parameter 'q'"}), 400

    articles = Article.query.filter(
        (Article.title.ilike(f"%{query}%")) |
        (Article.content.ilike(f"%{query}%"))
    ).all()

    result = [
        {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author_id': article.author_id,
            'author_username': article.author.username
        }
        for article in articles
    ]
    return jsonify(result), 200
