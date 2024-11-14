from flask import Flask
from .extensions import db
from .main.routes import main

# Cria e configura a aplicação Flask
def create_app():
    app = Flask(__name__)
    
    # Configura a aplicação usando o arquivo 'config.Config'
    app.config.from_object('app.config.Config')

    # Inicializa a extensão de banco de dados
    db.init_app(app)

    # Registra o blueprint 'main' com as rotas
    app.register_blueprint(main)

    return app
