import pytest
from unittest.mock import patch
import requests
import unittest.mock
from quality_control import create_app
import time

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        yield client

def test_health_check(client):
    """Teste para verificar se o serviço de health check está rodando corretamente."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "Service running"}

@patch('requests.post')
def test_process_voucher_success(mock_post, client):
    """Teste para processar o voucher com sucesso."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "Voucher processed"}

    data = {
        "contactId": "mC05TsH79PtxaPjP5eMu",
        "cpf": "06681013260",
        "voucher": "FIDELA",
    }

    response = client.post('/restHelper/processVoucher', json=data)
    assert response.status_code == 200
    assert response.json == {"status": "Voucher processed"}

@patch('requests.post')
def test_process_voucher_redundancy(mock_post, client):
    """Teste para simular uma falha de conexão e verificar redundância."""
    mock_post.side_effect = [
        requests.exceptions.ConnectionError,
        unittest.mock.Mock(status_code=200, json=lambda: {"status": "Voucher processed"})
    ]

    data = {
        "contactId": "mC05TsH79PtxaPjP5eMu",
        "cpf": "06681013260",
        "voucher": "FIDELA",
    }

    response = client.post('/restHelper/processVoucher', json=data)
    assert response.status_code == 500
    assert response.json == {"error": ""}

@patch('requests.post')
def test_persist_loyalty_substitution(mock_post, client):
    """Teste para simular substituição de falha com timeout."""
    mock_post.side_effect = [
        requests.exceptions.Timeout,
        unittest.mock.Mock(status_code=200, json=lambda: {"status": "Loyalty persisted"})
    ]

    data = {
        "firstName": "Stella",
        "lastName": "Fogaça",
        # Outros dados...
        "cpf": "01080070494",
        "loyaltyMobileOS": "OpenBSD 6",
        "loyaltyMobileOSVersion": "1.4.0",
    }

    response = client.post('/restHelper/persistLoyalty', json=data)
    assert response.status_code == 500
    assert response.json == {"error": ""}

@patch('requests.post')
def test_persist_loyalty_prediction_prevention(mock_post, client):
    """Teste para verificar predição e prevenção de falhas ao persistir lealdade."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "Loyalty persisted"}

    data = {
        "firstName": "Stella",
        "lastName": "Fogaça",
        # Outros dados...
        "cpf": "01080070494",
        "loyaltyMobileOS": "OpenBSD 6",
        "loyaltyMobileOSVersion": "1.4.0",
    }

    start_time = time.time()
    response = client.post('/restHelper/persistLoyalty', json=data)
    end_time = time.time()

    assert response.status_code == 200
    assert end_time - start_time < 2.0
