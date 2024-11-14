from locust import HttpUser, task, between

'''
Define um usuário de teste de carga para simular requisições à API de notícias.
'''
class NoticiasUser(HttpUser):
    '''
    Tempo de espera entre as tarefas (de 1 a 5 segundos).
    '''
    wait_time = between(1, 5)

    '''
    Tarefa para obter todas as notícias.
    '''
    @task
    def get_noticias(self):
        self.client.get("/noticias")

    '''
    Tarefa para criar uma nova notícia com dados de teste.
    '''
    @task
    def create_noticia(self):
        self.client.post("/noticias", json={
            "id": 3,
            "titulo": "Notícia de Teste de Carga",
            "texto": "Texto da notícia de teste de carga"
        })

    '''
    Tarefa para obter uma notícia específica pelo ID.
    '''
    @task
    def get_noticia(self):
        self.client.get("/noticias/3")

    '''
    Tarefa para atualizar uma notícia existente com dados de teste.
    '''
    @task
    def update_noticia(self):
        self.client.put("/noticias/3", json={
            "titulo": "Título Atualizado por Carga",
            "texto": "Texto atualizado por teste de carga"
        })

    '''
    Tarefa para deletar uma notícia específica pelo ID.
    '''
    @task
    def delete_noticia(self):
        self.client.delete("/noticias/3")
