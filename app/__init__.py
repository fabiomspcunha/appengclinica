from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializa o banco de dados
db = SQLAlchemy()

def create_app():
    # Criação do aplicativo Flask
    app = Flask(__name__)

    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manutencao.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
   # Inicializa o banco de dados com a aplicação
    db.init_app(app)

    migrate = Migrate(app,db)

    with app.app_context():
        db.create_all()

    # Importa os modelos (depois de inicializar o banco de dados)
    from .models import Equipamento, Manutencao

    # Importa e registra as rotas
    from .routes import main
    app.register_blueprint(main)

    return app
