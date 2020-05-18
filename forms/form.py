from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    #contas_id = StringField('ID', validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    preco = StringField('Preço', validators=[DataRequired()])
    data_venc = StringField('Data Venc', validators=[DataRequired()])
    comment = StringField('Comentário')
    submit = SubmitField('Gravar')