from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import app_active, app_config
config = app_config[app_active]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class ContasModel(db.Model):
    __tablename__ = 'contas'
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(80), nullable=True)
    preco = db.Column(db.Float(precision=2), nullable=True)
    data_venc = db.Column(db.Date(), nullable=True)
    comment = db.Column(db.Text(80))


if __name__ == '__main__':
    manager.run()