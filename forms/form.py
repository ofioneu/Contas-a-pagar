from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateTimeField, SubmitField, TextAreaField, DateField, BooleanField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    descricao = StringField('Descrição:', validators=[DataRequired()])
    preco = StringField('Valor:', validators=[DataRequired(message="Somente numeros e .")])
    data_venc = DateField('Data Venc:', validators=[DataRequired(message="Use - para separar a data! (09-02-1991")], format='%Y-%m-%d')
    comment = StringField('Comentário:')
    date_pesquise = StringField('Data venc:')
    descricao_pesquise = StringField('Descrição:')
    preco_pesquise = StringField('Valor:')
    comment_pesquise = StringField('Comentário:')
    submit = SubmitField('Gravar')
    submit_pesquise = SubmitField('Pesquisar')


     