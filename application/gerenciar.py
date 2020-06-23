from flask import Flask, render_template, redirect, Blueprint, url_for
from forms.form import MyForm
from models.db_contas import db, ContasModel
from app import app_config

from flask_mail import Mail, Message


gerenciar = Blueprint('gerenciar', __name__, template_folder='templates')

app = Flask(__name__, template_folder='templates')

mail = Mail(app)

@gerenciar.route('/', methods=['GET', 'POST'])
def home():
    form=MyForm()
    conta = ContasModel.query.all()    
    return render_template('home.html', form=form,  contas=conta)

@gerenciar.route('/post', methods=['GET', 'POST'])
def post():
    form = MyForm()
    #estou pegando as informações dos formularios
    if form.validate_on_submit:
        descricao = form.descricao.data
        preco = form.preco.data
        data_venc = form.data_venc.data
        comment = form.comment.data     
        #aqui é onde as informações serão enviadas para o banco
        contas=ContasModel(descricao,preco, data_venc, comment)
        db.session.add(contas)        
        db.session.commit()
        #aqui é selecionado todas as informações do banco e salvo em alldata
        alldata = ContasModel.query.all()
        listalldata=[]
        for i in alldata:
            listalldata.append(i.descricao)
            listalldata.append(i.preco)
            listalldata.append(i.data_venc)
            listalldata.append(i.comment)
        print(listalldata)
        #send_mail()
    
    return redirect('/')
@gerenciar.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    print("UPDATE")
    form_up = MyForm()
    if form_up.validate_on_submit:        
        item=ContasModel.query.get_or_404(id)
        item.descricao = form_up.descricao.data
        item.preco = form_up.preco.data     
        item.data_venc = form_up.data_venc.data
        item.comment = form_up.comment.data     
        #aqui é onde as informações serão enviadas para o banco
        print('Descriçao: ', item.descricao)
        print("Preço: ", item.preco) 
        print("Data_venc: ", item.data_venc) 
        print("Comentário: ", item.comment)    
        db.session.commit()
    return redirect('/')

@gerenciar.route('/select/', methods=['GET', 'POST'])
def select():
    form = MyForm()
    #if form.validate_on_submit:
    filtro=form.filtro.data
    print('Filtro: ', filtro)
    item=ContasModel.query.filter_by(data_venc = filtro).all()
    for i in item:
        print(i.descricao)
    
        #return render_template('editar.html',form_up = form_up, item =item)
    return redirect(url_for('gerenciar.home'))


@gerenciar.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_contas(id):
    delete = ContasModel.query.get_or_404(id)
    db.session.delete(delete)
    db.session.commit()

    return redirect ('/')




def send_mail():
   msg = Message('Hello', sender = "conta.casa89@gmail.com", recipients = ["fmfabio.0991@yahoo.com.br"])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"