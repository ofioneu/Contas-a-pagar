from flask import Flask, render_template, redirect, Blueprint, url_for
from forms.form import MyForm, ListaHome
from models.db_contas import db, ContasModel, HistoryModel
from app import app_config
from sqlalchemy import func
import datetime
from datetime import datetime
import babel



crud = Blueprint('crud', __name__, template_folder='templates')

@crud.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    form_lista = ListaHome()
    conta = ContasModel.query.order_by(ContasModel.data_venc.asc())
    return render_template('home.html', form=form, form_lista=form_lista, contas=conta, soma=soma())


@crud.route('/post', methods=['GET', 'POST'])
def post():
    form = MyForm()
    # estou pegando as informações dos formularios
    if form.validate_on_submit:
        descricao = form.descricao.data
        preco = form.preco.data
        data_venc = form.data_venc.data
        date = datetime.strptime(data_venc, '%d/%m/%Y').date()
        print('data_venc: ', date)
        comment = form.comment.data
        # aqui é onde as informações serão enviadas para o banco
        contas = ContasModel(descricao, preco, date, comment)
        historico_contas = HistoryModel(descricao, preco, date, comment)
        db.session.add(contas)
        db.session.add(historico_contas)
        db.session.commit()
    return redirect('/')


@crud.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form_up = ListaHome()
    if form_up.validate_on_submit:
        item = ContasModel.query.get_or_404(id)
        item_historico = HistoryModel.query.get_or_404(id)
        item.descricao = form_up.list_descr.data
        item.preco = form_up.list_preco.data
        date_list=form_up.list_date.data
        date = datetime.strptime(date_list, '%d/%m/%Y').date()
        item.data_venc=date
        item.comment = form_up.list_comment.data

        #atualiza o histórico
        item_historico = HistoryModel.query.get_or_404(id)
        item_historico.descricao = form_up.list_descr.data
        item_historico.preco = form_up.list_preco.data
        date_list=form_up.list_date.data
        date = datetime.strptime(date_list,'%d/%m/%Y').date()
        item_historico.data_venc=date        
        item_historico.comment = form_up.list_comment.data
        # aqui é onde as informações serão enviadas para o banco
        db.session.commit()
    return redirect('/')


@crud.route('/select/', methods=['GET', 'POST'])
def select():
    form = MyForm()
    if form.validate_on_submit:
        descricao = form.descricao_pesquise.data
        preco = form.preco_pesquise.data
        try:
            date = form.date_pesquise_ini.data
            date_f = form.date_pesquise_fim.data
        except:
            pass
        comment = form.comment_pesquise.data
        if descricao:
            descricao_pesquise = "%{}%".format(descricao)
            item2 = ContasModel.query.filter(ContasModel.descricao.like(descricao_pesquise)).all()
            return render_template('return_filtro.html', item=item2, soma = soma_filtro(ContasModel.descricao, descricao_pesquise, None))

        elif preco:
            print('p')
            item1 = ContasModel.query.filter_by(preco=preco).all()
            return render_template('return_filtro.html', item=item1, soma=soma_filtro(ContasModel.preco, preco, None))

        elif date and date_f:
            date_format = datetime.strptime(date,'%d/%m/%Y').date()
            datef_format = datetime.strptime(date_f,'%d/%m/%Y').date()
            item = ContasModel.query.filter(ContasModel.data_venc.between(date_format, datef_format))
            return render_template('return_filtro.html', item=item, soma=soma_filtro(ContasModel.data_venc, date_format, datef_format))

        elif comment:
            print('coment')
            comment_pesquise = "%{}%".format(comment)
            item3 = ContasModel.query.filter(ContasModel.comment.like(comment_pesquise)).all()
            return render_template('return_filtro.html', item=item3, soma=soma_filtro(ContasModel.comment, comment_pesquise, None))
        else:
            return render_template('no_data.html')

@crud.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_contas(id):
    delete = ContasModel.query.get_or_404(id)
    db.session.delete(delete)
    db.session.commit()
    return redirect('/')



# funções que retornam somatoria do campo preco
def soma():
    soma =  ContasModel.query.filter_by(preco=ContasModel.preco).all()
    somatoriaVet = []    
    for i in soma:
        valorStr =str(i.preco)
        valorFormat = babel.numbers.parse_decimal(valorStr, locale='pt_BR')
        somatoriaVet.append(float(valorFormat))
    somatoria = sum(somatoriaVet)
    return somatoria

def soma_filtro(campo, date_format, datef_format):
    print('campo: ', campo)
    if campo == 'preco':
        resultado = ContasModel.query.filter_by(preco=campo).all()
        somatoriaVet = []
        for i in resultado:
            valorStr =str(i.preco)
            valorFormat = babel.numbers.parse_decimal(valorStr, locale='pt_BR')
            somatoriaVet.append(float(valorFormat))
        somatoria = sum(somatoriaVet)
        return somatoria
    elif campo == ContasModel.data_venc:
        resultado = ContasModel.query.filter(ContasModel.data_venc.between(date_format, datef_format))
        somatoriaVet=[]
        for i in resultado:
            valorStr =str(i.preco)
            valorFormat = babel.numbers.parse_decimal(valorStr, locale='pt_BR')
            somatoriaVet.append(float(valorFormat))
        somatoria = sum(somatoriaVet)
        return somatoria
    else:
        resultado = ContasModel.query.filter(campo.like(date_format)).all()
        somatoriaVet=[]
        for i in resultado:
            valorStr =str(i.preco)
            valorFormat = babel.numbers.parse_decimal(valorStr, locale='pt_BR')
            somatoriaVet.append(float(valorFormat))
        somatoria = sum(somatoriaVet)
        return somatoria


