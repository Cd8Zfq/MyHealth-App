from flask import Blueprint

bp = Blueprint('main', __name__)

from app.routes import public, auth, patient, doctor
