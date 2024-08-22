from db import db
from sqlalchemy import LargeBinary
from flask_login import UserMixin

class Agendamentos(db.Model):
    __tablename__ = 'agendamento'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    dateContato = db.Column(db.Integer, nullable=True)
    dateContatoResp = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Integer, nullable=False)
    deposito = db.Column(db.String(3), nullable=True)
    cnpj = db.Column(db.Integer, nullable=False)
    fornecedor = db.Column(db.String, nullable=False)
    numeroPedido = db.Column(db.Integer(6), nullable=False, unique=True)
    observacao = db.Column(db.String, nullable=True)
    volumePallets = db.Column(db.Integer, nullable=True)
    volumeCxs = db.Column(db.Integer, nullable=True)
    arquivo = db.Column(LargeBinary, nullable=True)
    
    divergencias = db.relationship('Divergencias', backref='agendamento', uselist=False, cascade='all, delete-orphan')
    trocas = db.relationship('Trocas', backref='agendamento', uselist=False, cascade='all, delete-orphan')
    devolucoes = db.relationship('Devolucoes', backref='agendamento', uselist=False, cascade='all, delete-orphan')
    recebimento = db.relationship('Recebimento', backref='agendamento', uselist=False, cascade='all, delete-orphan')

class Divergencias(db.Model):
    __tablename__ = 'divergencias'
    id = db.Column(db.Integer, db.ForeignKey('agendamento.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    diverg = db.Column(db.Boolean, default=False)
    divergMotivo = db.Column(db.String, nullable=True)
    divergObs = db.Column(db.String, nullable=True)

class Trocas(db.Model):
    __tablename__ = 'trocas'
    id = db.Column(db.Integer, db.ForeignKey('agendamento.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    trocas = db.Column(db.Boolean, default=False)
    trocasObs = db.Column(db.String, nullable=True)
    trocasValor = db.Column(db.Float, nullable=True)

class Devolucoes(db.Model):
    __tablename__ = 'devolucoes'
    id = db.Column(db.Integer, db.ForeignKey('agendamento.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    devolucoes = db.Column(db.Boolean, default=False)
    devolucoesObs = db.Column(db.String, nullable=True)
    devolucoesValor = db.Column(db.Float, nullable=True)

class Recebimento(db.Model):
    __tablename__ = 'recebimento'
    id = db.Column(db.Integer, db.ForeignKey('agendamento.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    recebimento = db.Column(db.Boolean, default=False)
    recebimentObs = db.Column(db.String, nullable=True)
    recebQtdePallets = db.Column(db.Integer, nullable=True)
    recebQtdeChapas = db.Column(db.Integer, nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    userNome = db.Column(db.String, unique=True)
    userEmail = db.Column(db.String, unique=True)
    userSenha = db.Column(db.String, nullable=False)
    userToken = db.Column(db.Integer, nullable=True)
    userAdm = db.Column(db.Boolean, nullable=True)