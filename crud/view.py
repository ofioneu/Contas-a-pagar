from flask import Flask, render_template, redirect, Blueprint, url_for
from forms.form import MyForm, ListaHome
from models.db_contas import db, ContasModel, HistoryModel
from app import app_config
from sqlalchemy import func, desc
import datetime
from datetime import datetime
import babel
import json



crud = Blueprint('crud', __name__, template_folder='templates')

@crud.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    form_lista = ListaHome()
    conta = ContasModel.query.order_by(ContasModel.data_venc.asc())
    
    list_status =[]
    for i in conta:
        if(i.pago != str(1)):
            list_status.append(i)
    return render_template('home.html', form=form, form_lista=form_lista, contas=list_status, soma=soma())

@crud.route('/venc', methods=['GET'])
def venc():
    vence_hj = ContasModel.query.filter(ContasModel.data_venc == datetime.now().date()).all()
    venc={}
    tam = len(vence_hj)
    for i, j in zip(range(0,tam), vence_hj):
        venc['descricao'+str(i)]=j.descricao
    print('jjjj', venc)
    return json.dumps(venc)


@crud.route('/post', methods=['GET', 'POST'])
def post():
    form = MyForm()
    # estou pegando as informações dos formularios
    if form.validate_on_submit:
        descricao = form.descricao.data
        preco = form.preco.data
        data_venc = form.data_venc.data
        date = datetime.strptime(data_venc, '%d/%m/%Y').date()
        comment = form.comment.data
        status_pg = form.status_pg.data
        # aqui é onde as informações serão enviadas para o banco
        contas = ContasModel(descricao, preco, date, comment, status_pg)
        data_alt = datetime.now()
        historico_contas = HistoryModel(descricao, preco, date, comment, status_pg, data_alt)
        db.session.add(contas)
        db.session.add(historico_contas)
        db.session.commit()
    return redirect('/')


@crud.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    print('ID =', id)
    form_up = ListaHome()
    if form_up.validate_on_submit:
        item = ContasModel.query.get_or_404(id)
        #item_historico = HistoryModel.query.get_or_404(id)
        item.descricao = form_up.list_descr.data
        item.preco = form_up.list_preco.data
        date_list=form_up.list_date.data
        date = datetime.strptime(date_list, '%d/%m/%Y').date()
        item.data_venc=date
        item.comment = form_up.list_comment.data
        if(item.pago == '0' and form_up.status_pg.data==True):
            item.pago = form_up.status_pg.data

        #atualiza o histórico
        descricao = form_up.list_descr.data
        preco = form_up.list_preco.data
        date_list=form_up.list_date.data
        date = datetime.strptime(date_list,'%d/%m/%Y').date()
        comment = form_up.list_comment.data
        pago = form_up.status_pg.data
        data_alt = datetime.now()
        historico_contas = HistoryModel(descricao, preco, date, comment, pago, data_alt)
        db.session.add(historico_contas)
        # aqui é onde as informações serão enviadas para o banco
        db.session.commit()
    return redirect('/')


@crud.route('/select/', methods=['GET', 'POST'])
def select():
    form = MyForm()
    if form.validate_on_submit:
        descricao = form.descricao_pesquise.data
        preco = form.preco_pesquise.data
        pago = form.status_pg_pesquise.data
        try:
            date = form.date_pesquise_ini.data
            date_f = form.date_pesquise_fim.data
        except:
            pass
        comment = form.comment_pesquise.data
        if descricao:
            descricao_pesquise = "%{}%".format(descricao)
            item2 = ContasModel.query.filter(ContasModel.descricao.like(descricao_pesquise)).all()
            form_lista = ListaHome()
            list_status =[]
            for i in item2:
                if(i.pago != str(1)):
                    list_status.append(i)
            return render_template('return_filtro.html', item=list_status, form_lista=form_lista, contas=item2, soma = soma_filtro(ContasModel.descricao, descricao_pesquise, None))

        elif preco:
            item1 = ContasModel.query.filter(ContasModel.preco.like(preco)).all()
            form_lista = ListaHome()
            list_status =[]
            for i in item1:
                if(i.pago != str(1)):
                    list_status.append(i)
            return render_template('return_filtro.html', item=list_status, form_lista=form_lista, contas=item1, soma=soma_filtro(ContasModel.preco, preco, None))

        elif date and date_f:
            date_format = datetime.strptime(date,'%d/%m/%Y').date()
            datef_format = datetime.strptime(date_f,'%d/%m/%Y').date()
            item = ContasModel.query.filter(ContasModel.data_venc.between(date_format, datef_format))
            form_lista = ListaHome()
            list_status =[]
            for i in item:
                if(i.pago != str(1)):
                    list_status.append(i)
            print('list_pago: ', list_status)

            return render_template('return_filtro.html', item=list_status, form_lista=form_lista, contas=item, soma=soma_filtro(ContasModel.data_venc, date_format, datef_format))

        elif comment:
            print('coment')
            comment_pesquise = "%{}%".format(comment)
            item3 = ContasModel.query.filter(ContasModel.comment.like(comment_pesquise)).all()
            form_lista = ListaHome()
            list_status =[]
            for i in item3:
                if(i.pago != str(1)):
                    list_status.append(i)
            return render_template('return_filtro.html', item=list_status, form_lista=form_lista, contas=item3, soma=soma_filtro(ContasModel.comment, comment_pesquise, None))
        
        elif pago:
            item4 = ContasModel.query.filter(ContasModel.pago =='1').order_by(desc(ContasModel.data_venc))
            form_lista = ListaHome()
            list_status =[]
            for i in item4:
                if(i.pago != str(1)):
                    list_status.append(i)
            return render_template('return_filtro.html', item=list_status, form_lista=form_lista, contas=item4, soma=soma_filtro(ContasModel.pago, pago, None), form =form)
        
        else:
            conta = ContasModel.query.order_by(ContasModel.data_venc.asc())
            form_lista = ListaHome()
            list_status =[]
            for i in conta:
                if(i.pago != str(1)):
                    list_status.append(i)
        return render_template('return_filtro.html', item=list_status, form_lista=form_lista, contas=conta, soma=soma(), form =form)


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
    elif campo == ContasModel.pago:
        resultado = ContasModel.query.filter(ContasModel.pago=='1')
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


