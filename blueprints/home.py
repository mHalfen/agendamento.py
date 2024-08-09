from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models import Agendamentos, Divergencias, Trocas, Devolucoes, Recebimento
from datetime import datetime

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
def home():
    dataHoje = datetime.today().date()
    agendamentos = db.session.query(Agendamentos).filter(Agendamentos.date == dataHoje).all()
    return render_template('home.html', agendamentos=agendamentos)


@home_bp.route('/home/novoAgendamento', methods=['GET', 'POST'])
def home_novoAgendamento():
    dataHoje = datetime.today().date()

    if request.method == 'GET':
        return render_template('home_novoAgendamento.html')
    
    elif request.method == 'POST':
        dateContato = dataHoje
        dateContatoResp = request.form['dateContatoRespForm']
        date = request.form['dateForm']
        deposito = request.form['depositoForm']
        cnpj = request.form['cnpjForm']
        fornecedor = request.form['fornecedorForm']
        numeroPedido = request.form['numeroPedidoForm']
        observacao = request.form['obsForm']
        volumePallets = request.form['volumePalletsForm']
        volumeCxs = request.form['volumeCxsForm']

        novoAgendamento = Agendamentos(
            dateContato = dateContato,
            dateContatoResp = dateContatoResp,
            date = date,
            deposito = deposito,
            cnpj = cnpj,
            fornecedor = fornecedor,
            numeroPedido = numeroPedido,
            observacao = observacao,
            volumePallets = volumePallets,
            volumeCxs = volumeCxs)
        
        db.session.add(novoAgendamento)
        db.session.commit()      
    return redirect(url_for('home.home_novoAgendamento'))


@home_bp.route('/home/visualizarAgendamento')
def home_visualizarAgendamento():
    dataFiltrada = request.args.get('date')

    if dataFiltrada:
        dataFiltrada = datetime.strptime(dataFiltrada, '%Y-%m-%d').date()
        agendamentos = db.session.query(Agendamentos).filter(Agendamentos.date == dataFiltrada).all()
    else:
        agendamentos = db.session.query(Agendamentos).all()
    return render_template('home_visualizarAgendamento.html', agendamentos=agendamentos)


@home_bp.route('/home/visualizarAgendamento/editar/<int:id>', methods=['GET', 'POST'])
def home_visualizarAgendamento_editar(id):
    agendamentos = db.session.query(Agendamentos).filter_by(id=id).first()

    if request.method == 'GET':
        novaDiverg = db.session.query(Agendamentos).filter_by(id=id).first()

        if not novaDiverg:
            novaDiverg = Divergencias()

        return render_template('editarAgendamento.html', agendamentos=agendamentos, novaDiverg=novaDiverg)
    
    elif request.method == 'POST':
        agendamentos.dateContatoResp = request.form['dateContatoRespForm']
        agendamentos.date = request.form['dateForm']
        agendamentos.deposito = request.form['depositoForm']
        agendamentos.cnpj = request.form['cnpjForm']
        agendamentos.fornecedor = request.form['fornecedorForm']
        agendamentos.numeroPedido = request.form['numeroPedidoForm']
        agendamentos.observacao = request.form['obsForm']
        agendamentos.volumePallets = request.form['volumePalletsForm']
        agendamentos.volumeCxs = request.form['volumeCxsForm']

        novaDiverg = db.session.query(Divergencias).filter_by(id=id).first()
        
        if novaDiverg:
            novaDiverg.diverg = request.form['divergForm']
            novaDiverg.divergMotivo = request.form['divergMotivoForm']
            novaDiverg.divergObs = request.form['divergObsForm']
        else:
            novaDiverg = Divergencias(
                id=id,
                diverg=request.form['divergForm'],
                divergMotivo=request.form['divergMotivoForm'],
                divergObs=request.form['divergObsForm']
            )

        db.session.add(novaDiverg)
        db.session.commit()
        return redirect (url_for('home.home_visualizarAgendamento'))


@home_bp.route('/home/visualizarAgendamento/deletar/<int:id>')
def home_visualizarAgendamento_deletar(id):
    agendamentos = db.session.query(Agendamentos).filter_by(id=id).first()
    db.session.delete(agendamentos)
    db.session.commit()
    return redirect (url_for('home.home_visualizarAgendamento'))