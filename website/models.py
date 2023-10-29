from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# represents a Baby Buds user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    is_parent = db.Column(db.Boolean) # revisit this w Alder
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    products = db.relationship('Product', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    profile_pic = db.Column(db.String(100), default="flowers.png")

# represents a post in the Forum
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)

# represents a comment on a Post in the Forum
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)
    
# represents a product in the Marketplace
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(20))
    age = db.Column(db.String(32), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String(200))
    img = db.Column(db.String(200))

# # represents a parent user with a unique username and email
# class Parent(db.Model, UserMixin):
#     id = db.Column(db.Integer)
#     email = db.Column(db.String(100), primary_key=True)
#     username = db.Column(db.String(20), unique=True)
#     password = db.Column(db.String(100))
#     posts = db.relationship('Post', backref='parent', passive_deletes=True)
#     products = db.relationship('Product', backref='parent', passive_deletes=True)
#     can_comment = db.Column(db.Boolean, default=False)
#     profile_pic = db.Column(db.String(100), default="flowers.png")
    
# # represents an expert user with a unique email
# class Expert(db.Model, UserMixin):
#     id = db.Column(db.Integer)
#     email = db.Column(db.String(100), primary_key=True)
#     name = db.Column(db.String(20))
#     password = db.Column(db.String(100))
#     comments = db.relationship('Comment', backref='expert', passive_deletes=True)
#     can_comment = db.Column(db.Boolean, default=True)