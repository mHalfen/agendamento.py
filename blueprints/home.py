from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response, flash
from flask_login import login_required
from db import db
from models import Agendamentos, Divergencias, Trocas, Devolucoes, Recebimento, Fornecedores
from datetime import datetime
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'pdf'}

home_bp = Blueprint('home', __name__)
login_bp = Blueprint('login', __name__)

def allowed_file(filename):
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@home_bp.route('/suggestions')
def suggestions():
    termo = request.args.get('termo', '')
    if termo:
        fornecedores = db.session.query(Fornecedores.fornecedCnpj, Fornecedores.fornecedRazaoSocial).filter(Fornecedores.fornecedCnpj.like(f'%{termo}%')).all()
        suggestions = [{'cnpj': f[0], 'razao_social': f[1]} for f in fornecedores]
        return jsonify(suggestions)
    return jsonify([])


@home_bp.route('/home')
@login_required
def home():
    dataHoje = datetime.today().date()
    agendamentos = db.session.query(Agendamentos).filter(Agendamentos.date == dataHoje).all()
    return render_template('home.html', agendamentos=agendamentos)


@home_bp.route('/home/novoAgendamento', methods=['GET', 'POST'])
@login_required
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
        
        flash('Agendamento incluido com sucesso.', 'agendSucess')

        db.session.add(novoAgendamento)
        db.session.commit()
    return redirect(url_for('home.home_novoAgendamento'))


@home_bp.route('/home/visualizarAgendamento')
@login_required
def home_visualizarAgendamento():
    dataFiltrada = request.args.get('date')

    if dataFiltrada:
        dataFiltrada = datetime.strptime(dataFiltrada, '%Y-%m-%d').date()
        agendamentos = db.session.query(Agendamentos).filter(Agendamentos.date == dataFiltrada).all()
    else:
        agendamentos = db.session.query(Agendamentos).all()
    return render_template('home_visualizarAgendamento.html', agendamentos=agendamentos)


@home_bp.route('/home/visualizarAgendamento/upload', methods=['POST'])
def home_visualizarAgendamento_upload():
    # Recupera o ID do agendamento do formulário
    agendamento_id = request.form.get('agendamento_id')
    
    # Verifica se o campo 'file' está presente nos arquivos enviados
    if agendamento_id and 'file' in request.files:
        file = request.files['file']
        
        # Verifica se o arquivo tem um nome e se é permitido
        if file.filename != '' and allowed_file(file.filename):
            # Lê o conteúdo do arquivo
            file_content = file.read()
            
            # Encontra o agendamento correspondente no banco de dados
            agendamento = db.session.query(Agendamentos).get(agendamento_id)
            if agendamento:
                # Atualiza o campo 'arquivo' com o conteúdo do arquivo
                agendamento.arquivo = file_content
                db.session.commit()  # Salva as alterações no banco de dados

    
    # Redireciona de volta à página de visualização de agendamentos
    return redirect(url_for('home.home_visualizarAgendamento'))


@home_bp.route('/home/visualizarAgendamento/arquivo/<int:agendamento_id>')
@login_required
def home_visualizarAgendamento_view_upload(agendamento_id):
    agendamento = db.session.query(Agendamentos).get(agendamento_id)
    if agendamento and agendamento.arquivo:
        return Response(
            agendamento.arquivo,
            mimetype='application/pdf',
            headers={"Content-Disposition": f"inline; filename=arquivo_{agendamento_id}.pdf"}
        )
    return redirect(url_for('home.home_visualizarAgendamento'))


@home_bp.route('/home/visualizarAgendamento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def home_visualizarAgendamento_editar(id):
    agendamentos = db.session.query(Agendamentos).filter_by(id=id).first()
    novaDiverg = db.session.query(Divergencias).filter_by(id=id).first()
    novaTroca = db.session.query(Trocas).filter_by(id=id).first()
    novaDevolucao = db.session.query(Devolucoes).filter_by(id=id).first()
    novoRecebimento = db.session.query(Recebimento).filter_by(id=id).first()

    if request.method == 'GET':
        novaDiverg = db.session.query(Divergencias).filter_by(id=id).first()
        novaTroca = db.session.query(Trocas).filter_by(id=id).first()
        novaDevolucao = db.session.query(Devolucoes).filter_by(id=id).first()
        novoRecebimento = db.session.query(Recebimento).filter_by(id=id).first()

        if not novaDiverg:
            novaDiverg = Divergencias()
            
        if not novaTroca:
            novaTroca = Trocas()

        if not novaDevolucao:
            novaDevolucao = Devolucoes()

        if not novoRecebimento:
            novoRecebimento = Recebimento()

        return render_template('editarAgendamento.html',
                               agendamentos = agendamentos,
                               novaDiverg = novaDiverg,
                               novaTroca = novaTroca,
                               novaDevolucao = novaDevolucao,
                               novoRecebimento = novoRecebimento)
    
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
        novaTroca = db.session.query(Trocas).filter_by(id=id).first()
        novaDevolucao = db.session.query(Devolucoes).filter_by(id=id).first()
        novoRecebimento = db.session.query(Recebimento).filter_by(id=id).first()
        
        if novaDiverg:
            novaDiverg.diverg = bool(request.form.get('divergForm'))
            novaDiverg.divergMotivo = request.form['divergMotivoForm']
            novaDiverg.divergObs = request.form['divergObsForm']
        else:
            novaDiverg = Divergencias(
                id=id,
                diverg=bool(request.form.get('divergForm')),
                divergMotivo=request.form['divergMotivoForm'],
                divergObs=request.form['divergObsForm']
            )
            db.session.add(novaDiverg)

        if novaTroca:
            novaTroca.trocas = bool(request.form.get('trocasForm'))
            novaTroca.trocasObs = request.form['trocasObsForm']
            novaTroca.trocasValor = request.form['trocasValorForm']
        else:
            novaTroca = Trocas(
                id=id,
                trocas=bool(request.form.get('trocasForm')),
                trocasObs=request.form['trocasObsForm'],
                trocasValor='0'
            )
            db.session.add(novaTroca)

        if novaDevolucao:
            novaDevolucao.devolucoes = bool(request.form.get('devolucoesForm'))
            novaDevolucao.devolucoesObs = request.form['devolucoesObsForm']
            novaDevolucao.devolucoesValor = request.form['devolucoesValorForm']
        else:
            novaDevolucao = Devolucoes(
                id=id,
                devolucoes = bool(request.form.get('devolucoesForm')),
                devolucoesObs = request.form['devolucoesObsForm'],
                devolucoesValor = '0'
            )
            db.session.add(novaDevolucao)

        if novoRecebimento:
            novoRecebimento.recebimento = bool(request.form.get('recebimentoForm'))
            novoRecebimento.recebimentObs = request.form['recebimentObsForm']
            novoRecebimento.recebQtdePallets = request.form['recebQtdePalletsForm']
            novoRecebimento.recebQtdeChapas = request.form['recebQtdeChapasForm']
        else:
            novoRecebimento = Recebimento(
                id=id,
                recebimento = bool(request.form.get('recebimentoForm')),
                recebimentObs = request.form['recebimentObsForm'],
                recebQtdePallets = request.form['recebQtdePalletsForm'],
                recebQtdeChapas = request.form['recebQtdeChapasForm']
            )
            db.session.add(novoRecebimento)

        db.session.commit()
        return redirect (url_for('home.home_visualizarAgendamento'))


@home_bp.route('/home/visualizarAgendamento/deletar/<int:id>')
@login_required
def home_visualizarAgendamento_deletar(id):
    agendamentos = db.session.query(Agendamentos).filter_by(id=id).first()
    db.session.delete(agendamentos)
    db.session.commit()
    return redirect (url_for('home.home_visualizarAgendamento'))