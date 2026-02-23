from flask import render_template, redirect, request, make_response
from app.routes import bp

@bp.route('/')
def index():
    """Public landing page."""
    return render_template('index.html')

@bp.route('/set-lang/<lang>')
def set_lang(lang):
    """
    Language switcher endpoint.

    The user clicks a FR or EN button anywhere in the app, which sends a GET
    request here (e.g. /set-lang/en).  We validate the value, set a long-lived
    cookie, then redirect back to whatever page the user was on.

    The cookie is read on every request in the before_request hook inside
    create_app() and stored in g.lang, which the t() helper then uses to pick
    the correct language from the TRANSLATIONS dict in app/i18n.py.
    """
    # Reject any value that isn't a supported language code
    if lang not in ('fr', 'en'):
        lang = 'fr'

    # Redirect back to the referring page, or fall back to the home page
    response = make_response(redirect(request.referrer or '/'))

    # Store the chosen language in a cookie that lasts one year (in seconds)
    response.set_cookie('lang', lang, max_age=365 * 24 * 60 * 60)

    return response
