from flask import Flask, render_template, redirect, Blueprint
import requests
import json
from forms.form import MyForm
from models.db_contas import db, ContasModel


from models.db_contas import ContasModel


gerenciar = Blueprint('gerenciar', __name__, template_folder='templates')



@gerenciar.route('/', methods=['GET', 'POST'])
def home():
    form=MyForm()
    conta = ContasModel.query.all()
    
    return render_template('home.html', form=form, contas=conta)

@gerenciar.route('/post', methods=['GET', 'POST'])
def post():
    form = MyForm()
    if form.validate_on_submit:
        nome = form.nome.data
        preco = form.preco.data
        data_venc = form.data_venc.data
        comment = form.comment.data
        contas=ContasModel(nome,preco, data_venc, comment)
        db.session.add(contas)
        db.session.commit()      
    return redirect('/')

@gerenciar.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_contas(id):
    delete = ContasModel.query.get_or_404(id)
    db.session.delete(delete)
    db.session.commit()

    return redirect ('/')
