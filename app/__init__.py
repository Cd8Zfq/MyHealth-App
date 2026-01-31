from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'
login.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Blueprint registration - Unified
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models

@login.user_loader
def load_user(id):
    from app.models.user import User
    return User.query.get(int(id))