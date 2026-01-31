from flask import render_template
from app.routes import bp

@bp.route('/')
def index():
    """
    Page d'accueil publique.
    Affiche la landing page avec les informations générales.
    """
    return render_template('index.html')
