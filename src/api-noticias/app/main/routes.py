from flask import Blueprint, jsonify, request
from app.services.noticia_service import (
    get_all_noticias, get_noticia_by_id, add_noticia,
    update_noticia, delete_noticia_service
)

# Criação do blueprint 'main' para as rotas da aplicação
main = Blueprint('main', __name__)

# Rota GET para obter todas as notícias
@main.route('/noticias', methods=['GET'])
def get_noticias():
    noticias = get_all_noticias()
    return jsonify([noticia.to_dict() for noticia in noticias])

# Rota POST para criar uma nova notícia
@main.route('/noticias', methods=['POST'])
def create_noticia():
    data = request.json
    noticia = add_noticia(data)
    return jsonify(noticia.to_dict()), 201

# Rota GET para obter uma notícia pelo ID
@main.route('/noticias/<int:id>', methods=['GET'])
def get_noticia(id):
    noticia = get_noticia_by_id(id)
    if noticia:
        return jsonify(noticia.to_dict())
    return jsonify({'error': 'Notícia não encontrada'}), 404

# Rota PUT para atualizar uma notícia pelo ID
@main.route('/noticias/<int:id>', methods=['PUT'])
def edit_noticia(id):
    data = request.json
    noticia = update_noticia(id, data)
    if noticia:
        return jsonify(noticia.to_dict())
    return jsonify({'error': 'Notícia não encontrada'}), 404

# Rota DELETE para remover uma notícia pelo ID
@main.route('/noticias/<int:id>', methods=['DELETE'])
def delete_noticia(id):
    if delete_noticia_service(id):
        return jsonify({'message': 'Notícia removida com sucesso'})
    return jsonify({'error': 'Notícia não encontrada'}), 404
