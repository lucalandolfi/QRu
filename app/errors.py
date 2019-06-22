from flask import render_template
from . import app

@app.errorhandler(401)
def not_authorized(e):
    return render_template('errors/401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
