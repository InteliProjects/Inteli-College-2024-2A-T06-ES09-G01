from app import create_app
from app.extensions import db

'''
app contém a aplicação criada usando a função create_app
'''
app = create_app()

'''
Cria o contexto da aplicação para realizar operações dentro desse contexto
'''
with app.app_context():
    '''
    Cria todas as tabelas do banco de dados, se elas não existirem
    '''
    db.create_all()

'''
Se o script for executado diretamente, inicia o servidor com debug habilitado
'''
if __name__ == '__main__':
    app.run(debug=True)
