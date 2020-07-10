from flask import Flask, render_template, redirect, Blueprint, url_for
from forms.form import MyForm
from models.db_contas import db, ContasModel
from app import app_config
from sqlalchemy import func

from flask_mail import Mail, Message


gerenciar = Blueprint('gerenciar', __name__, template_folder='templates')

app = Flask(__name__, template_folder='templates')

mail = Mail(app)


@gerenciar.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    conta = ContasModel.query.all()
    return render_template('home.html', form=form,  contas=conta, soma=soma())


@gerenciar.route('/post', methods=['GET', 'POST'])
def post():
    form = MyForm()
    # estou pegando as informações dos formularios
    if form.validate_on_submit:
        descricao = form.descricao.data
        preco = form.preco.data
        data_venc = form.data_venc.data
        comment = form.comment.data
        # aqui é onde as informações serão enviadas para o banco
        contas = ContasModel(descricao, preco, data_venc, comment)
        db.session.add(contas)
        db.session.commit()
        # aqui é selecionado todas as informações do banco e salvo em alldata
        alldata = ContasModel.query.all()
        listalldata = []
        for i in alldata:
            listalldata.append(i.descricao)
            listalldata.append(i.preco)
            listalldata.append(i.data_venc)
            listalldata.append(i.comment)
        print(listalldata)
        # send_mail()

    return redirect('/')


@gerenciar.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form_up = MyForm()
    if form_up.validate_on_submit:
        item = ContasModel.query.get_or_404(id)
        item.descricao = form_up.descricao.data
        item.preco = form_up.preco.data
        item.data_venc = form_up.data_venc.data
        item.comment = form_up.comment.data
        # aqui é onde as informações serão enviadas para o banco
        db.session.commit()
    return redirect('/')


@gerenciar.route('/select/', methods=['GET', 'POST'])
def select():
    form = MyForm()
    # if form.validate_on_submit:
    descricao = form.descricao_pesquise.data
    preco = form.preco_pesquise.data
    date = form.date_pesquise.data
    comment = form.comment_pesquise.data
    if descricao:
        descricao_pesquise = "%{}%".format(descricao)
        item2 = ContasModel.query.filter(ContasModel.descricao.like(descricao_pesquise)).all()
        return render_template('return_filtro.html', item=item2, soma = soma_filtro(ContasModel.descricao, descricao_pesquise))

    elif preco:
        item1 = ContasModel.query.filter_by(preco=preco).all()
        return render_template('return_filtro.html', item=item1, soma=soma_filtro(ContasModel.preco, preco))

    elif date:
        data_pesquise = "%{}%".format(date)
        item = ContasModel.query.filter(
            ContasModel.data_venc.like(data_pesquise)).all()
        return render_template('return_filtro.html', item=item, soma=soma_filtro(ContasModel.data_venc, data_pesquise))

    elif comment:
        comment_pesquise = "%{}%".format(comment)
        item3 = ContasModel.query.filter(ContasModel.comment.like(comment_pesquise)).all()
        return render_template('return_filtro.html', item=item3, soma=soma_filtro(ContasModel.comment, comment_pesquise))
    else:
       return render_template('no_data.html')


@gerenciar.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_contas(id):
    delete = ContasModel.query.get_or_404(id)
    db.session.delete(delete)
    db.session.commit()

    return redirect('/')


def send_mail():
   msg = Message('Hello', sender="conta.casa89@gmail.com",
                 recipients=["fmfabio.0991@yahoo.com.br"])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

# funções que retornam somatoria do campo preco
def soma():
    soma = db.session.query(func.sum(ContasModel.preco))
    i=0
    for i in soma:
        pass
    return i

def soma_filtro(campo, data_form):
    print('campo: ', campo)
    if campo == 'preco':
        resultado = ContasModel.query.filter_by(preco=preco).all()
        valor=0
        for i in resultado:
            valor += i.preco
        return valor
    else:
        resultado = ContasModel.query.filter(campo.like(data_form)).all()
        valor=0
        for i in resultado:
            valor += i.preco
        return valor
