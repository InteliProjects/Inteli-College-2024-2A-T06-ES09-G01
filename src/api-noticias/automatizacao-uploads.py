import os
import requests
import random
import time

'''
URL da API para deletar notícias.
'''
API_UPLOAD_URL = 'http://localhost:5000/restHelper/persistLoyalty'  

'''
Caminho da pasta para uploads (não utilizado neste trecho).
'''
FOLDER_PATH = 'src/ecm_backend/uploads'  

'''
Número total de uploads a serem realizados.
'''
NUM_UPLOADS = 1000  
i = 0

'''
Loop para realizar múltiplas requisições DELETE à API para deletar notícias.
'''
while NUM_UPLOADS > 0:
    data = {
  "firstName": "Stella",
  "lastName": "Fogaça",
  "phone": "(46) 97275-4341",
  "birthdate": "1999-11-11",
  "street": "Travessa Felipe da Costa",
  "district": "Park Place",
  "city": "Itatinga",
  "state": "SE",
  "country": "Montenegro",
  "postalCode": "46311-420",
  "addressNumber": "4441",
  "addressComplement": "",
  "email": "rubin@medhurst-casper.test",
  "facebookId": "georgeanna.bartell",
  "googleId": "kay.bartell",
  "firebaseId": "7b2fa6e8-89e8-4083-aa82-328bc6bb63cb",
  "messagingToken": "2c25c749fa8de3bccd65400ea0890d8665fa775fd20e90a37e26d3c42a9c3f516f14e50eb18a87ef430449b67c3eb595a38b6b3087b9bc4dfac46336fd26361b",
  "topics": "General",
  "cpf": "01080070494",
  "userCategory": "Agricultor",
  "loyaltyMobileOS": "OpenBSD 6",
  "loyaltyMobileOSVersion": "1.4.0",
  "loyaltyMobileBundleVersion": "7.3.4"
}
    response = requests.post(API_UPLOAD_URL, json=data)  # Realiza a requisição DELETE para a URL da API com o ID i.
    
    if response.status_code == 200:  # Verifica se a resposta foi bem-sucedida (status 201).
        NUM_UPLOADS -= 1  # Decrementa o número de uploads restantes.
        i += 1  # Incrementa o ID.
        print(f'Upload {i} realizado com sucesso')  # Exibe mensagem de sucesso.
    else:
        print(f'Erro ao realizar upload {i}')  # Exibe mensagem de erro se a resposta não for bem-sucedida.
