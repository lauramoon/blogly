"""Models for Blogly."""
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import backref

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.Text, nullable=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref=backref('posts', cascade='all, delete-orphan'))

    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    @property
    def pretty_datetime(self):
        return self.created_at.strftime("%b %d, %Y %I:%M %p")

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(50), nullable=False, unique=True)

class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)