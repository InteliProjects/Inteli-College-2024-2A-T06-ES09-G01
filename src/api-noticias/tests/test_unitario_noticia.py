import unittest
from app import create_app, db
from app.models.noticia import Noticia

'''
Classe de teste para o modelo Noticia.
'''
class NoticiaTestCase(unittest.TestCase):
    
    '''
    Configura o ambiente de teste antes de cada teste ser executado.
    '''
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usa um banco de dados em memória para os testes.
        self.client = self.app.test_client()  # Cria um cliente de teste para simular requisições.

        '''
        Dentro do contexto da aplicação, cria todas as tabelas necessárias no banco de dados.
        '''
        with self.app.app_context():
            db.create_all()

    '''
    Limpa o ambiente de teste após cada teste ser executado.
    '''
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()  # Remove a sessão atual do banco de dados.
            db.drop_all()  # Apaga todas as tabelas do banco de dados.

    '''
    Testa se a rota '/noticias' retorna todas as notícias com um status HTTP 200.
    '''
    def test_get_all_noticias(self):
        response = self.client.get('/noticias')
        self.assertEqual(response.status_code, 200)  # Verifica se o status de resposta é 200 (OK).

'''
Executa os testes quando o script é executado diretamente.
'''
if __name__ == '__main__':
    unittest.main()
