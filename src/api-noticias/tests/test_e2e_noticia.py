import pytest
import requests

# URL base da API para os testes
BASE_URL = "http://127.0.0.1:5000"

# Fixture do pytest que fornece um exemplo de notícia para os testes
@pytest.fixture
def noticia_exemplo():
    return {
        "id": 3,
        "titulo": "Notícia de Teste",
        "texto": "Texto da notícia de teste"
    }

# Teste para obter todas as notícias
def test_get_noticias():
    response = requests.get(f"{BASE_URL}/noticias")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Teste para criar uma nova notícia
def test_create_noticia(noticia_exemplo):
    response = requests.post(f"{BASE_URL}/noticias", json=noticia_exemplo)
    assert response.status_code == 201
    assert response.json()["titulo"] == noticia_exemplo["titulo"]

# Teste para obter uma notícia específica pelo ID
def test_get_noticia_by_id(noticia_exemplo):
    requests.post(f"{BASE_URL}/noticias", json=noticia_exemplo)
    response = requests.get(f"{BASE_URL}/noticias/{noticia_exemplo['id']}")
    assert response.status_code == 200
    assert response.json()["titulo"] == noticia_exemplo["titulo"]

# Teste para atualizar uma notícia existente
def test_update_noticia(noticia_exemplo):
    requests.post(f"{BASE_URL}/noticias", json=noticia_exemplo)
    updated_data = {"titulo": "Título Atualizado", "texto": "Texto Atualizado"}
    response = requests.put(f"{BASE_URL}/noticias/{noticia_exemplo['id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["titulo"] == "Título Atualizado"

# Teste para deletar uma notícia
def test_delete_noticia(noticia_exemplo):
    requests.post(f"{BASE_URL}/noticias", json=noticia_exemplo)
    response = requests.delete(f"{BASE_URL}/noticias/{noticia_exemplo['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Notícia removida com sucesso"
