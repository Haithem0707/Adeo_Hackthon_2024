# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from markupsafe import Markup
import re

db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):
    with app.app_context():
        def initialize_database():
            db.create_all()
        initialize_database()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    
    @app.template_filter('highlight')
    def highlight(text, query):
        if not query:
            return text
        # Use regex for case-insensitive replacement
        escaped_query = re.escape(query)
        highlighted_text = re.sub(f'({escaped_query})', r'<span class="highlight">\1</span>', text, flags=re.IGNORECASE)
        return Markup(highlighted_text)

    return app
