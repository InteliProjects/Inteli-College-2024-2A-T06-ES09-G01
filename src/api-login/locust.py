# Importa as bibliotecas necessárias para o Locust
from locust import HttpUser, TaskSet, task, between

# Define o comportamento do usuário durante o teste de carga
class UserBehavior(TaskSet):
    
    @task
    def login(self):
        """
        Simula o login de um usuário enviando uma requisição POST
        para o endpoint /login com um payload JSON.
        """
        self.client.post("/login", json={"username": "testuser", "password": "testpass"})

# Define a classe do usuário que executará as tarefas definidas acima
class WebsiteUser(HttpUser):
    """
    Representa o usuário simulado pelo Locust, executando as tarefas da classe UserBehavior.
    """
    tasks = [UserBehavior]
    wait_time = between(1, 2)
