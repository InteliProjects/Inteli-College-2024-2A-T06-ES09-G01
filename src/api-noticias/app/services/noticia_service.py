from app.models.noticia import Noticia
from app.extensions import db

# Função para obter todas as notícias
def get_all_noticias():
    return Noticia.query.all()

# Função para obter uma notícia pelo ID
def get_noticia_by_id(id):
    return Noticia.query.get(id)

# Função para adicionar uma nova notícia
def add_noticia(data):
    noticia = Noticia(id=data.get('id'), titulo=data['titulo'], texto=data['texto'])
    db.session.add(noticia)
    db.session.commit()
    return noticia

# Função para atualizar uma notícia existente
def update_noticia(id, data):
    noticia = Noticia.query.get(id)
    if noticia:
        noticia.titulo = data['titulo']
        noticia.texto = data['texto']
        db.session.commit()
        return noticia
    return None

# Função para deletar uma notícia pelo ID
def delete_noticia_service(id):
    noticia = Noticia.query.get(id)
    if noticia:
        db.session.delete(noticia)
        db.session.commit()
        return True
    return False
