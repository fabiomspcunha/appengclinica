from flask import Blueprint, render_template, request, redirect, url_for
from .models import Equipamento, Manutencao, ordens_servico
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
    equipamentos = Equipamento.query.all()  # Pega os equipamentos do inventário
    return render_template('os.html', equipamentos=equipamentos, ordens=ordens_servico)


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

@main.route('/add_os', methods=['POST'])
def add_ordem():
    equipamento_id = request.form['equipamento']
    descricao = request.form['descricao']

    # Verifica se o equipamento existe no banco de dados
    equipamento = Equipamento.query.get(equipamento_id)
    
    if not equipamento:
        print("Erro: Equipamento não encontrado!")
        return redirect(url_for('main.os_page'))  # Redireciona de volta à página de OS

    status = "Aberto"
    ordem = {
        'id': len(ordens_servico) + 1,
        'equipamento': equipamento.nome,  # Agora pegamos o nome do equipamento do BD
        'descricao': descricao,
        'status': status
    }

    ordens_servico.append(ordem)
    return redirect(url_for('main.index'))


@main.route('/update/<int:ordem_id>', methods=['POST'])
def update_ordem(ordem_id):
    for ordem in ordens_servico:
        if ordem['id'] == ordem_id:
            ordem['status'] = request.form['status']
            break
    return redirect(url_for('main.index'))

@main.route('/delete/<int:ordem_id>')
def delete_ordem(ordem_id):
    global ordens_servico
    ordens_servico = [ordem for ordem in ordens_servico if ordem['id'] != ordem_id]
    return redirect(url_for('main.index'))