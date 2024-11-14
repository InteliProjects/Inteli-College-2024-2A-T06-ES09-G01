from app.extensions import db

# Modelo Noticia, representando a tabela 'noticia' no banco de dados
class Noticia(db.Model):
    # Coluna 'id' como chave primária
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    
    # Coluna 'titulo' como string de até 120 caracteres, não nula
    titulo = db.Column(db.String(120), nullable=False)
    
    # Coluna 'texto' como campo de texto, não nulo
    texto = db.Column(db.Text, nullable=False)

    # Converte a instância da classe Noticia em um dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'texto': self.texto
        }
