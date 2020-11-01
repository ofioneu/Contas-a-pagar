from flask import Flask, render_template, redirect, Blueprint, url_for
from forms.form import Historico
from models.db_contas import db, HistoryModel, ContasModel
from app import app_config
from sqlalchemy import func
import babel
import datetime
from datetime import datetime

history = Blueprint('history', __name__, template_folder='templates')


@history.route('/history/', methods=['GET', 'POST'])
def historico():
    form = Historico()
    valor_history=soma_history()
    his = HistoryModel.query.order_by(HistoryModel.data_venc.asc())
    return render_template('history.html', form=form, item=his, soma_history=valor_history)

@history.route('/select_history/', methods=['GET', 'POST'])
def historico_filtro():
    form = Historico()
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
            item2 = HistoryModel.query.filter(HistoryModel.descricao.like(descricao_pesquise)).all()
            return render_template('history.html', item=item2, soma_history = soma_filtro_history(HistoryModel.descricao, descricao_pesquise, None), form =form)

        elif preco:
            item1 = HistoryModel.query.filter_by(preco=preco).all()
            return render_template('history.html', item=item1, soma_history=soma_filtro_history(HistoryModel.preco, preco, None), form =form)

        elif date and date_f:
            date_format = datetime.strptime(date,'%d/%m/%Y').date()
            datef_format = datetime.strptime(date_f,'%d/%m/%Y').date()
            item = HistoryModel.query.filter(HistoryModel.data_venc.between(date_format, datef_format))
            return render_template('history.html', item=item, soma_history=soma_filtro_history(HistoryModel.data_venc, date_format, datef_format ), form=form)

        elif comment:
            comment_pesquise = "%{}%".format(comment)
            print(comment_pesquise)
            item3 = HistoryModel.query.filter(HistoryModel.comment.like(comment_pesquise)).all()
            return render_template('history.html', item=item3, soma_history=soma_filtro_history(HistoryModel.comment, comment_pesquise, None), form =form)
        elif pago:
            print('pago= ',pago)
            item4 = HistoryModel.query.filter(HistoryModel.pago.is_(pago)).all()
            return render_template('history.html', item=item4, soma_history=soma_filtro_history(HistoryModel.pago, pago, None), form =form)

        else:
            return render_template('no_data.html')



def soma_history():
    soma =  ContasModel.query.filter_by(preco=ContasModel.preco).all()
    somatoriaVet = []    
    for i in soma:
        valorStr =str(i.preco)
        valorFormat = babel.numbers.parse_decimal(valorStr, locale='pt_BR')
        somatoriaVet.append(float(valorFormat))
    somatoria = sum(somatoriaVet)
    return somatoria


def soma_filtro_history(campo, date_format, datef_format):
    if campo == 'preco':
        resultado = HistoryModel.query.filter_by(preco=campo).all()
        somatoriaVet = []
        for i in resultado:
           valorStr =str(i.preco)
           valorFormat = babel.numbers.parse_decimal(valorStr, locale='pt_BR')
           somatoriaVet.append(float(valorFormat))
        somatoria = sum(somatoriaVet)
        return somatoria
    elif campo == HistoryModel.data_venc:
        resultado = HistoryModel.query.filter(HistoryModel.data_venc.between(date_format, datef_format))
        somatoriaVet=[]
        for i in resultado:
            valorStr =str(i.preco)
            valorFormat = babel.numbers.parse_decimal(valorStr, locale='pt_BR')
            somatoriaVet.append(float(valorFormat))
        somatoria = sum(somatoriaVet)
        return somatoria
        
    elif campo == HistoryModel.pago:
        resultado = HistoryModel.query.filter(HistoryModel.pago=='1')
        somatoriaVet=[]
        for i in resultado:
            valorStr =str(i.preco)
            print("valor str: ", valorStr)
            valorFormat = babel.numbers.parse_decimal(valorStr, locale='pt_BR')
            somatoriaVet.append(float(valorFormat))
        print("vet: ", somatoriaVet)
        somatoria = sum(somatoriaVet)
        print("Somatória: ", somatoria)
        return somatoria
    else:
        resultado = HistoryModel.query.filter(campo.like(date_format)).all()
        somatoriaVet=[]
        for i in resultado:
            valorStr =str(i.preco)
            valorFormat = babel.numbers.parse_decimal(valorStr, locale='pt_BR')
            somatoriaVet.append(float(valorFormat))
        somatoria = sum(somatoriaVet)
        return somatoria
