from db import db

class Agendamentos(db.Model):
    __tablename__ = 'agendamento'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    dateContato = db.Column(db.Integer, nullable=True)
    dateContatoResp = db.Column(db.String, nullable=True)
    date = db.Column(db.Integer, nullable=False)
    deposito = db.Column(db.String, nullable=True)
    cnpj = db.Column(db.Integer, nullable=False)
    fornecedor = db.Column(db.String, nullable=False)
    numeroPedido = db.Column(db.Integer, nullable=False, unique=True)
    observacao = db.Column(db.String, nullable=True)
    volumePallets = db.Column(db.Integer, nullable=True)
    volumeCxs = db.Column(db.Integer, nullable=True)
    
    divergencias = db.relationship('Divergencias', backref='agendamento', uselist=False, cascade='all, delete-orphan')
    trocas = db.relationship('Trocas', backref='agendamento', uselist=False, cascade='all, delete-orphan')
    devolucoes = db.relationship('Devolucoes', backref='agendamento', uselist=False, cascade='all, delete-orphan')
    recebimento = db.relationship('Recebimento', backref='agendamento', uselist=False, cascade='all, delete-orphan')

class Divergencias(db.Model):
    __tablename__ = 'divergencias'
    id = db.Column(db.Integer, db.ForeignKey('agendamento.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    diverg = db.Column(db.String, nullable=True)
    divergMotivo = db.Column(db.String, nullable=True)
    divergObs = db.Column(db.String, nullable=True)

class Trocas(db.Model):
    __tablename__ = 'trocas'
    id = db.Column(db.Integer, db.ForeignKey('agendamento.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    trocas = db.Column(db.String, nullable=True)
    trocasObs = db.Column(db.String, nullable=True)
    trocasValor = db.Column(db.Integer, nullable=True)

class Devolucoes(db.Model):
    __tablename__ = 'devolucoes'
    id = db.Column(db.Integer, db.ForeignKey('agendamento.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    devolucoes = db.Column(db.String, nullable=True)
    devolucoesObs = db.Column(db.String, nullable=True)
    devolucoesValor = db.Column(db.Integer, nullable=True)

class Recebimento(db.Model):
    __tablename__ = 'recebimento'
    id = db.Column(db.Integer, db.ForeignKey('agendamento.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    recebimento = db.Column(db.String, nullable=True)
    recebimentObs = db.Column(db.String, nullable=True)
    recebQtdePallets = db.Column(db.Integer, nullable=True)
    recebQtdeChapas = db.Column(db.Integer, nullable=True)

