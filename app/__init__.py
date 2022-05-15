from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()
def create_app(config_name):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URL'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # creating app configuration
    app.config.from_object(config_options[config_name])
    
    # registering blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # initializing flask extensions
    db.init_app(app)
    
    return app
