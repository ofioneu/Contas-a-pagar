from flask import Flask
from config import app_config, app_active
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from application.gerenciar import gerenciar

config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'
    db = SQLAlchemy(config.APP)
    migrate = Migrate(app, db)

    db.init_app(app)

    app.register_blueprint(gerenciar)

    return app