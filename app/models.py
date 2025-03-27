from . import db
from datetime import datetime


ordens_servico = []

# Tabela de Equipamentos
class Equipamento(db.Model):
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    fabricante = db.Column(db.String(50), nullable=False)
    num_serie = db.Column(db.String(50), unique=True, nullable=False)
    localizacao = db.Column(db.String(50), nullable=False)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    manutencoes = db.relationship('Manutencao', backref='equipamento', lazy=True)

    def __repr__(self):
        return f'<Equipamento {self.nome}>'

# Tabela de Manutenções
class Manutencao(db.Model):
    __tablename__ = 'manutencoes'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    tecnico_responsavel = db.Column(db.String(100), nullable=False)
    custo = db.Column(db.Float, nullable=True)

    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), nullable=False)

    def __repr__(self):
        return f'<Manutencao {self.tipo} - {self.descricao}>'
