from flask import Blueprint, jsonify, request
from app.models import Article, User, db


article_bp = Blueprint('articles', __name__)


@article_bp.route('/', methods=['POST'])
def create_article():
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        author_id = data.get('author_id')

        if not title or not content or not author_id:
            return jsonify({'message': 'Missing required fields'}), 400

        author = User.query.get(author_id)
        if not author:
            return jsonify({'message': 'Author not found'}), 404

        article = Article(title=title, content=content, author_id=author_id)
        db.session.add(article)
        db.session.commit()

        return jsonify({'message': 'Article created successfully'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@article_bp.route('/', methods=['GET'])
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
def get_one_article(id):
    article = Article.query.get(id)
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
def update_article(id):
    data = request.get_json()
    article = Article.query.get(id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404

    if 'title' in data:
        article.title = data['title']
    if 'content' in data:
        article.content = data['content']

    db.session.commit()
    return jsonify({'message': 'Article updated successfully'}), 200


@article_bp.route('/<int:id>', methods=['DELETE'])
def delete_article(id):
    article = Article.query.get(id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404

    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': 'Article deleted successfully'}), 200
