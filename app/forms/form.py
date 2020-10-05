from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateTimeField, SubmitField, TextAreaField, DateField, BooleanField, FloatField
from wtforms.validators import DataRequired
from wtforms import validators

class MyForm(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(message='Esse campo é obrigatório')])
    preco = StringField('Valor:', [validators.NumberRange(min=0.1, max=1000000.0, message="Somente numeros e .")])
    data_venc = StringField('Data Venc:', [validators.DataRequired(message="09/02/1991 = 09021991")])
    comment = StringField('Comentário:')
    date_pesquise_ini = StringField('Data inicio:')
    date_pesquise_fim = StringField('Data fim:')
    descricao_pesquise = StringField('Descrição:')
    preco_pesquise = StringField('Valor:')
    comment_pesquise = StringField('Comentário:')
    submit = SubmitField('Gravar')
    submit_pesquise = SubmitField('Pesquisar')

class Historico(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(message='Esse campo é obrigatório')])
    preco = StringField('Valor:', [validators.NumberRange(min=0.1, max=1000000.0, message="Somente numeros e .")])
    data_venc = StringField('Data Venc:', [validators.NumberRange(min=8, max=8, message="09/02/1991 = 09021991")])
    comment = StringField('Comentário:')
    date_pesquise_ini = StringField('Data inicio:')
    date_pesquise_fim = StringField('Data fim:')
    descricao_pesquise = StringField('Descrição:')
    preco_pesquise = StringField('Valor:')
    comment_pesquise = StringField('Comentário:')
    submit = SubmitField('Gravar')
    submit_pesquise = SubmitField('Pesquisar')

class ListaHome(FlaskForm):
    list_descr = StringField('Descrição:')
    list_preco = StringField('Valor:')
    list_date = StringField('Data Venc:')
    list_comment = StringField('Comentário:')
    list_submit = SubmitField('Atualizar')



     