from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateTimeField, SubmitField, TextAreaField, DateField, BooleanField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    descricao = StringField('Descrição', validators=[DataRequired()])
    preco = StringField('Preço', validators=[DataRequired(message="Somente numeros e .")])
    data_venc = DateField('Data Venc', validators=[DataRequired(message="Use - para separar a data! (09-02-1991")], format='%Y-%m-%d')
    comment = StringField('Comentário')
    filtro = StringField('Filtro')
    submit = SubmitField('Gravar')


     