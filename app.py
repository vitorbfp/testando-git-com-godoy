from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL
import os
from dotenv import load_dotenv
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


app = Flask(__name__)


# -------------------------------
# Configuração do banco MySQL (Aiven)
# -------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://avnadmin:AVNS_y5iL2M2J8Vl4qFR3SCO@mysql-26d59920-vitorbfp.i.aivencloud.com:10984/defaultdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Parâmetros SSL
ssl_args = {
    'ssl': {
        'ssl_ca': './certificats/ca.pem'
,  # Caminho para o certificado CA fornecido pela Aiven
    }
}

db = SQLAlchemy(app, engine_options={"connect_args": ssl_args})

# -------------------------------
# Modelo para o banco de dados
# -------------------------------
class PalavraDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    significado = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


# Dicionário em memória
dicionario = {
'Goiania' : 'Capital do estado de Goiás, Brasil.',
'Paris' : 'Capital da França, famosa por sua arte, moda e cultura.',
'Berlim' : 'Capital da Alemanha, conhecida por sua história rica e cultura vibrante.',
'Tokyo' : 'Capital do Japão, famosa por sua tecnologia avançada e cultura única.',
'New York' : 'Cidade dos Estados Unidos, conhecida como a "Big Apple", famosa por seus arranha-céus e diversidade cultural.'
}



# -------------------------------
# Endpoints com dicionário estático
# -------------------------------


@app.route('/significado/<palavra>', methods=['GET'])
def get_significado(palavra):
    significado = dicionario.get(palavra)
    if significado:
        return significado  # retorna só o valor, como texto puro
    else:
        return 'Palavra não encontrada', 404



# Rota POST para adicionar uma nova palavra e significado
@app.route('/significado', methods=['POST'])
def adicionar_significado():
    dados = request.get_json()
    palavra = dados.get('palavra')
    significado = dados.get('significado')

    if not palavra or not significado:
        return 'Dados incompletos', 400

    dicionario[palavra] = significado
    return f'Significado de "{palavra}" adicionado com sucesso!', 201


# Rota PUT para atualizar o significado de uma palavra existente
@app.route('/significado/<palavra>', methods=['PUT'])
def atualizar_significado(palavra):
    dados = request.get_json()
    novo_significado = dados.get('significado')

    if palavra not in dicionario:
        return 'Palavra não encontrada', 404

    if not novo_significado:
        return 'Significado não fornecido', 400

    dicionario[palavra] = novo_significado
    return f'Significado de "{palavra}" atualizado com sucesso!', 200



# Rota DELETE para atualizar o significado de uma palavra existente
@app.route('/significado/<palavra>', methods=['DELETE'])
def deletar(palavra):

    if palavra not in dicionario:
        return 'Palavra não encontrada', 404

    else:
        del dicionario[palavra] 
        return f'{palavra} deletada com sucesso do dicionario!', 200





# -------------------------------
# Endpoints com banco de dados MySQL
# -------------------------------
@app.route('/bd/significado/<palavra>', methods=['GET'])
def get_significado_bd(palavra):
    resultado = PalavraDB.query.filter_by(nome=palavra).first()
    if resultado:
        return resultado.significado
    else:
        return 'Palavra não encontrada no banco', 404

@app.route('/bd/significado', methods=['POST'])
def adicionar_significado_bd():
    dados = request.get_json()
    palavra = dados.get('palavra')
    significado = dados.get('significado')

    if not palavra or not significado:
        return 'Dados incompletos', 400

    nova = PalavraDB(nome=palavra, significado=significado)
    db.session.add(nova)
    db.session.commit()
    return f'Significado de "{palavra}" adicionado ao banco com sucesso!', 201

@app.route('/bd/significado/<palavra>', methods=['PUT'])
def atualizar_significado_bd(palavra):
    dados = request.get_json()
    novo_significado = dados.get('significado')

    resultado = PalavraDB.query.filter_by(nome=palavra).first()
    if not resultado:
        return 'Palavra não encontrada no banco', 404

    resultado.significado = novo_significado
    db.session.commit()
    return f'Significado de "{palavra}" atualizado no banco com sucesso!', 200

@app.route('/bd/significado/<palavra>', methods=['DELETE'])
def deletar_bd(palavra):
    resultado = PalavraDB.query.filter_by(nome=palavra).first()
    if not resultado:
        return 'Palavra não encontrada no banco', 404

    db.session.delete(resultado)
    db.session.commit()
    return f'{palavra} deletada com sucesso do banco!', 200



# -------------------------------
# Inicialização da aplicação
# -------------------------------


if __name__ == '__main__':
    app.run(debug=True)