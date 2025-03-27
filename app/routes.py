from flask import Blueprint, render_template, request, redirect, url_for
from .models import Equipamento, Manutencao, ordens_servico
from . import db
from datetime import datetime, timedelta

# Define um blueprint para as rotas principais
main = Blueprint('main', __name__)

@main.route('/preventiva', methods=['GET'])
def mostrar_preventiva():
    equipamentos = Equipamento.query.all()  # Buscar todos os equipamentos
    manutencoes = Manutencao.query.all()  # Buscar todas as manutenções cadastradas
    return render_template('preventiva.html', equipamentos=equipamentos, manutencoes=manutencoes)


@main.route('/adicionar_manutencao', methods=['POST'])
def adicionar_manutencao():
    equipamento_id = request.form.get('equipamento_id')
    tipo = request.form.get('tipo')
    descricao = request.form.get('descricao')
    data = request.form.get('data')
    tecnico_responsavel = request.form.get('tecnico_responsavel')
    custo = request.form.get('custo')

    if not equipamento_id or not tipo or not descricao or not data or not tecnico_responsavel:
        return redirect(url_for('main.mostrar_preventiva'))

    try:
        nova_manutencao = Manutencao(
            equipamento_id=int(equipamento_id),
            tipo=tipo,
            descricao=descricao,
            data=datetime.strptime(data, '%Y-%m-%d'),
            tecnico_responsavel=tecnico_responsavel,
            custo=float(custo) if custo else None
        )
        db.session.add(nova_manutencao)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return redirect(url_for('main.mostrar_preventiva'))



@main.route('/')
def index():
    return render_template('index.html')

@main.route('/inventario')
def inventario():
    equipamentos = Equipamento.query.all()
    return render_template('inventario.html', equipamentos=equipamentos, timedelta=timedelta)

@main.route('/os')
def os():
    equipamentos = Equipamento.query.all()  # Pega os equipamentos do inventário
    
    # Define a prioridade dos status para ordenação
    def status_priority(status):
        prioridade = {"Aberto": 1, "Em andamento": 2, "Concluído": 3}
        return prioridade.get(status, 4)  # Se status desconhecido, recebe menor prioridade

    # Ordena as ordens de serviço pela prioridade do status
    ordens_ordenadas = sorted(ordens_servico, key=lambda ordem: status_priority(ordem['status']))

    return render_template('os.html', equipamentos=equipamentos, ordens=ordens_ordenadas)

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
    
    return redirect(url_for('main.inventario'))

@main.route('/equipamentos')
def listar_equipamentos():
    equipamentos = Equipamento.query.all()
    return render_template('equipamentos.html', equipamentos=equipamentos, timedelta=timedelta)

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
        return redirect(url_for('main.inventario'))

    return render_template('editar.html', equipamento=equipamento)

# Rota para deletar um equipamento
@main.route('/deletar/<int:id>', methods=['GET'])
def deletar(id):
    equipamento = Equipamento.query.get_or_404(id)
    db.session.delete(equipamento)
    db.session.commit()
    return redirect(url_for('main.inventario'))

@main.route('/add_os', methods=["POST","GET"])
def add_ordem():
    equipamento_id = request.form['equipamento']
    descricao = request.form['descricao']
    profissional = request.form['profissional']
    hora = request.form.get('hora')

    # Verifica se o equipamento existe no banco de dados
    equipamento = Equipamento.query.get(equipamento_id)
    
    if not equipamento:
        print("Erro: Equipamento não encontrado!")
        return redirect(url_for('main.os'))  # Redireciona de volta à página de OS

    status = "Aberto"
    
    ordem = {
        'id': len(ordens_servico) + 1,
        'equipamento': equipamento.nome,  # Agora pegamos o nome do equipamento do BD
        'descricao': descricao,
        'profissional': profissional,
        'status': status,
        'hora': hora
    }

    ordens_servico.append(ordem)
    return redirect(url_for('main.os'))

@main.route('/update/<int:ordem_id>', methods=['POST'])
def update_ordem(ordem_id):
    for ordem in ordens_servico:
        if ordem['id'] == ordem_id:
            ordem['status'] = request.form['status']
            break
    return redirect(url_for('main.os'))

@main.route('/delete/<int:ordem_id>')
def delete_ordem(ordem_id):
    global ordens_servico
    ordens_servico = [ordem for ordem in ordens_servico if ordem['id'] != ordem_id]
    return redirect(url_for('main.os'))

@main.route('/editar_manutencao/<int:id>', methods=['GET', 'POST'])
def editar_manutencao(id):
    manutencao = Manutencao.query.get_or_404(id)
    equipamentos = Equipamento.query.all()  # Para caso o usuário queira mudar o equipamento

    if request.method == 'POST':
        manutencao.equipamento_id = request.form.get('equipamento_id')
        manutencao.tipo = request.form.get('tipo')
        manutencao.descricao = request.form.get('descricao')
        manutencao.data = datetime.strptime(request.form.get('data'), '%Y-%m-%d')
        manutencao.tecnico_responsavel = request.form.get('tecnico_responsavel')
        manutencao.custo = float(request.form.get('custo')) if request.form.get('custo') else None

        db.session.commit()
        return redirect(url_for('main.mostrar_preventiva'))  # Redireciona para a lista de preventivas

    return render_template('editar_manutencao.html', manutencao=manutencao, equipamentos=equipamentos)

@main.route('/deletar_manutencao/<int:id>', methods=['GET'])
def deletar_manutencao(id):
    manutencao = Manutencao.query.get_or_404(id)

    db.session.delete(manutencao)
    db.session.commit()

    return redirect(url_for('main.mostrar_preventiva'))

