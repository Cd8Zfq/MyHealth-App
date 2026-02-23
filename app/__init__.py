from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# These are shared extension objects created outside the app factory.
# They are initialized later inside create_app() so the app can be
# created multiple times (useful for testing) without conflicts.
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

# Tell Flask-Login which route to redirect to when a @login_required
# page is accessed without being logged in.
login.login_view = 'main.login'
login.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)

    # Load configuration values (SECRET_KEY, DATABASE_URI, etc.) from config.py
    app.config.from_object(config_class)

    # Bind the extensions to this specific app instance
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # --- Internationalisation (i18n) setup ---
    # Import the translation helpers from app/i18n.py
    from app.i18n import t, tm

    # Register t() and tm() as Jinja2 globals so every template can call
    # {{ t('key') }} or {{ tm(measurement_type) }} without importing anything.
    app.jinja_env.globals['t'] = t
    app.jinja_env.globals['tm'] = tm

    # Before every request, read the 'lang' cookie (defaults to 'fr') and
    # store it in Flask's request-scoped g object.  The t() function reads
    # g.lang to decide which language to return.
    @app.before_request
    def set_language():
        g.lang = request.cookies.get('lang', 'fr')

    # Register the main blueprint that contains all application routes
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

# Import models here so SQLAlchemy discovers them when Alembic runs migrations.
# This must be after db is defined but outside create_app to avoid circular imports.
from app import models

# Tells Flask-Login how to reload a User object from the session cookie.
# It receives the user id stored in the session and must return the User object.
@login.user_loader
def load_user(id):
    from app.models.user import User
    return User.query.get(int(id))
