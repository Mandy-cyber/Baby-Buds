from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# set up database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    # encrypt cookies & session data, passwords
    app.config['SECRET_KEY'] = "reufijpweodsp"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    # blueprints group common routes
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()

    # login manager creates a session, default = 30 days
    lm = LoginManager()
    # redirects to login page if they are not logged in
    lm.login_view = "auth.login"
    lm.init_app(app)

    @lm.user_loader
    def load_user(id):
        return User.query.get(id)

    return app