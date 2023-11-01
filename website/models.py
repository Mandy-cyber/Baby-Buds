from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# represents a Baby Buds user
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    profile_pic = db.Column(db.String(100), default="flowers.png")
    user_type = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

# represents a Parent user with posts and products
class Parent(User):
    __tablename__ = 'parent'

    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    products = db.relationship('Product', backref='user', passive_deletes=True)

    __mapper_args__ = {'polymorphic_identity': 'parent_user'}

# represents an Expert user with comments
class Expert(User):
    __tablename__ = 'expert'

    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)

    __mapper_args__ = {'polymorphic_identity': 'expert_user'}

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