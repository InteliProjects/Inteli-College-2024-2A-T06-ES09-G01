import os

# Classe de configuração para a aplicação
class Config:
    # URI do banco de dados, obtida da variável de ambiente 'DATABASE_URL', ou SQLite por padrão
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    
    # Desabilita o rastreamento de modificações do SQLAlchemy para economizar recursos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
