"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE = "data:image/png;base64,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"


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True,
                          default=DEFAULT_IMAGE)
    
    post = db.relationship('Post', backref="user", cascade="all, delete-orphan")



class Post(db.Model):
    """User posts"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(15), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Tag(db.Model):
    """Tags for posts"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    post = db.relationship('Post', secondary="post_tags", backref="tags")


class PostTag(db.Model):
    """Joins posts and tags"""
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)