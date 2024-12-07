from flask import Blueprint, render_template, request, redirect, url_for
from .models import Equipamento, Manutencao
from . import db

# Define um blueprint para as rotas principais
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/inventario')
def inventario():
    equipamentos = Equipamento.query.all()
    return render_template('inventario.html', equipamentos=equipamentos)

@main.route('/os')
def os():
    return render_template('os.html')

@main.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('nome')
    modelo = request.form.get('modelo')
    fabricante = request.form.get('fabricante')
    num_serie = request.form.get('num_serie')
    localizacao = request.form.get('localizacao')

    novo_equipamento = Equipamento(
        nome=nome,
        modelo=modelo,
        fabricante=fabricante,
        num_serie=num_serie,
        localizacao=localizacao
    )


    db.session.add(novo_equipamento)
    db.session.commit()
    
    return redirect(url_for('main.index'))

@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    equipamento = Equipamento.query.get_or_404(id)

    if request.method == 'POST':
        equipamento.nome = request.form['nome']
        equipamento.modelo = request.form['modelo']
        equipamento.fabricante = request.form['fabricante']
        equipamento.num_serie = request.form['num_serie']
        equipamento.localizacao = request.form['localizacao']

        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('editar.html', equipamento=equipamento)

# Rota para deletar um equipamento
@main.route('/deletar/<int:id>', methods=['GET'])
def deletar(id):
    equipamento = Equipamento.query.get_or_404(id)
    db.session.delete(equipamento)
    db.session.commit()
    return redirect(url_for('main.index'))

