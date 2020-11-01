from flask_sqlalchemy import SQLAlchemy
from config import app_active, app_config
from sqlalchemy import func
from sqlalchemy.sql import select

config = app_config[app_active]
db = SQLAlchemy(config.APP)

class ContasModel(db.Model):
    __tablename__ = 'contas'
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(80), nullable=True)
    preco = db.Column(db.String(), nullable=True)
    data_venc = db.Column(db.Date(), nullable=True)
    comment = db.Column(db.Text(80))
    pago = db.Column(db.String(5))

    def __repr__(self):
        return '<ContasModel %r>' % self.id

    def __init__(self, descricao, preco, data_venc, comment, pago):
        self.descricao = descricao
        self.preco = preco
        self.data_venc = data_venc        
        self.comment = comment
        self.pago = pago


class HistoryModel(db.Model):
    __tablename__ = 'historico_contas'
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(80), nullable=True)
    preco = db.Column(db.String(), nullable=True)
    data_venc = db.Column(db.Date(), nullable=True)
    comment = db.Column(db.Text(80))
    pago = db.Column(db.String(5))
    data_alt = db.Column(db.Date())

    def __repr__(self):
        return '<HistoryModel %r>' % self.id

    def __init__(self, descricao, preco, data_venc, comment, pago, data_alt):
        self.descricao = descricao
        self.preco = preco
        self.data_venc = data_venc
        self.comment = comment
        self.pago = pago
        self.data_alt = data_alt
