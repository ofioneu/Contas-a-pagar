from flask import Flask
from config import app_config, app_active
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from application.gerenciar import gerenciar
from flask_mail import Mail


config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__, template_folder='templates', static_url_path='')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'
    db = SQLAlchemy(config.APP)
    migrate = Migrate(app, db)
    db.init_app(app)
    mail_serv=app.config['MAIL_SERVER']='smtp.gmail.com'
    mail_port=app.config['MAIL_PORT'] = 465
    mail_username=app.config['MAIL_USERNAME'] = 'conta.casa89@gmail.com'
    mail_pw=app.config['MAIL_PASSWORD'] = '@11tahe89'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True


    app.register_blueprint(gerenciar)

    return app