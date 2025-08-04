from flask import Flask

app = Flask(__name__)

# Dicionário em memória
dicionario = {
'pais': 'Brasile',
'cidade': 'São Paulo',
'bairro': 'Jardim Paulista',
'rua': 'Avenida Paulista',
'numero': '1578',
'cep': '01310-200',
'telefone': '(11) 1234-5678'
}

@app.route('/definition/<palavra>', methods=['GET'])
def get_significado(palavra):
    definition = dicionario.get(palavra)
    if definition:
        return definition  # retorna só o valor, como texto puro
    else:
        return 'Palavra não encontrada', 404

if __name__ == '__main__':
    app.run(debug=True)