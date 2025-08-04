from flask import Flask, request

app = Flask(__name__)

# Dicionário em memória
dicionario = {
'Goiania' : 'Capital do estado de Goiás, Brasil.',
'Paris' : 'Capital da França, famosa por sua arte, moda e cultura.',
'Berlim' : 'Capital da Alemanha, conhecida por sua história rica e cultura vibrante.',
'Tokyo' : 'Capital do Japão, famosa por sua tecnologia avançada e cultura única.',
'New York' : 'Cidade dos Estados Unidos, conhecida como a "Big Apple", famosa por seus arranha-céus e diversidade cultural.'
}

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



if __name__ == '__main__':
    app.run(debug=True)