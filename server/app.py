#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate
from models import db, Article

app = Flask(__name__)
app.secret_key = b'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200


@app.route('/articles/<int:id>')
def show_article(id):
    # test requires increment ALWAYS on every request
    session['page_views'] = session.get('page_views', 0) + 1

    # enforce limit AFTER increment
    if session['page_views'] > 3:
        return {'message': 'Maximum pageview limit reached'}, 401

    article = Article.query.get(id)

    # test expects existing article id=1 to return 200
    if article is None:
        return {'message': 'Article not found'}, 404

    return jsonify(article.to_dict()), 200


if __name__ == '__main__':
    app.run(port=5555)
