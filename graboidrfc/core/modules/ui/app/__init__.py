from flask import Flask

import json, os

def create_app(config_file='../configs.json', use_docker: bool = False):
    
    # Istanziamento di app e applicazione configurazione
    app = Flask(__name__)
    app.config.from_file(config_file, load=json.load)
    
    # Secret Key
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['USE_DOCKER'] = use_docker
    
    # Registrazione dei blueprints
    from .views.views import blueprint as views_blueprint
    app.register_blueprint(views_blueprint)
    
    from .views.handlers import blueprint as handlers_blueprint
    app.register_blueprint(handlers_blueprint)
    
    # Ritorno di app
    return app