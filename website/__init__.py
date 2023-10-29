from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    # encrypt cookies & session data, database information (passwords)
    app.config['SECRET_KEY'] = "reufijpweodsp"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Mom, Expert, Post, Comment, Product

    with app.app_context():
        db.create_all()

    lm = LoginManager()  # login manager creates a session, default = 30 days
    lm.login_view = "auth.login"  # redirects to login page if they are not logged in
    lm.init_app(app)

    @lm.user_loader
    def load_user(id):
        # load info about user given their id
        mom = Mom.query.filter_by(id=id)
        if mom:
            return Mom.query.get(int(id))

        expert = Expert.query.filter_by(id=id)
        if expert:
            return Expert.query.get(int(id))

    return app
