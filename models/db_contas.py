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
    data_venc = db.Column(db.String(8), nullable=True)
    comment = db.Column(db.Text(80))

    def __repr__(self):
        return '<ContasModel %r>' % self.id

    def __init__(self, descricao, preco, data_venc, comment):
        self.descricao = descricao
        self.preco = preco
        self.data_venc = data_venc        
        self.comment = comment
        
    
    def get(self):
        alldata = db.query.all()
        return alldata


    def find_contas(self, id):
        conta = db.query.filter_by(id=id).first()
        if conta:
            return conta
        return None

    def update_contas(self, descricao, preco, data_venc, comment):
        self.descricao = descricao
        self.preco = preco
        self.data_venc = data_venc
        self.comment = comment

    def delete_contas(self):
        db.session.delete(self)
        db.session.commit()

class HistoryModel(db.Model):
    __tablename__ = 'historico_contas'
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(80), nullable=True)
    preco = db.Column(db.String(), nullable=True)
    data_venc = db.Column(db.String(8), nullable=True)
    comment = db.Column(db.Text(80))

    def __repr__(self):
        return '<HistoryModel %r>' % self.id

    def __init__(self, descricao, preco, data_venc, comment):
        self.descricao = descricao
        self.preco = preco
        self.data_venc = data_venc        
        self.comment = comment
        
    
    def get(self):
        alldata = db.query.all()
        return alldata


    def find_contas(self, id):
        conta = db.query.filter_by(id=id).first()
        if conta:
            return conta
        return None
