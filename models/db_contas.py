from flask_sqlalchemy import SQLAlchemy
from config import app_active, app_config
from sqlalchemy import func

config = app_config[app_active]
db = SQLAlchemy(config.APP)

class ContasModel(db.Model):
    __tablename__ = 'contas'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(80), nullable=True)
    preco = db.Column(db.Float(precision=2), nullable=True)
    data_venc = db.Column(db.String(6), default=db.func.current_timestamp(), nullable=True)
    comment = db.Column(db.Text(80))

    def __repr__(self):
        return '<ContasModel %r>' % self.id

    def __init__(self, nome, preco, data_venc, comment):
        self.nome = nome
        self.preco = preco
        self.data_venc = data_venc
        self.comment = comment
        

    def json(self):
        return {
            'nome': self.nome,
            'preco': self.preco,
            'data_venc': self.data_venc,
            'comment': self.comment
        }


    def find_contas(self, id):
        conta = db.query.filter_by(id=id).first()
        if conta:
            return conta
        return None

    def update_contas(self, nome, preco, data_venc, comment):
        self.nome = nome
        self.preco = preco
        self.data_venc = data_venc

    def delete_contas(self):
        db.session.delete(self)
        db.session.commit()