from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

# Mom, Expert, Comment, Product, Post

class Mom(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=False)
    posts = db.relationship('Post', backref='mom', passive_deletes=True)
    products = db.relationship('Product', backref='mom', passive_deletes=True)
    profile_pic = db.Column(db.String(100), default="flowers.png")
    can_comment = db.Column(db.String(6), default="false")
    
    
class Expert(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    comments = db.relationship('Comment', backref='expert', passive_deletes=True)
    can_comment = db.Column(db.String(6), default="true")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    mauthor = db.Column(db.Integer, db.ForeignKey(
        'mom.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    category = db.Column(db.String(64), nullable=False)
    

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(20))
    age = db.Column(db.String(32), nullable=False)
    mauthor = db.Column(db.Integer, db.ForeignKey(
        'mom.id', ondelete="CASCADE"), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String(200))
    img = db.Column(db.String(200))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'expert.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)
