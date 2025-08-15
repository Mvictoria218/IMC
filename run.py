from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular_imc", methods=['POST'])   
def calcular_imc():
    nome = request.form["nome"]
    peso = request.form["peso"].replace(",", ".")
    altura = request.form["altura"].replace(",", ".")

    altura = float(altura)

    if altura > 3:  # Se digitou em centímetros
        altura = altura / 100

    imc_valor = round(float(peso) / (altura ** 2), 2)

    if imc_valor < 18.5:
        resultado = "Abaixo do peso"
    elif 18.5 <= imc_valor < 24.9:
        resultado = "Peso normal"
    elif 25 <= imc_valor < 29.9:
        resultado = "Sobrepeso"
    else:
        resultado = "Obesidade"

    caminho_arquivo = 'models/imc.txt'

    with open(caminho_arquivo, 'a') as arquivo:
        arquivo.write(f"{nome};{peso};{altura};{imc_valor};{resultado}\n")

    return redirect("/consultar")

@app.route("/consultar")
def consultar_imc():
    imc_list = []
    caminho_arquivo = 'models/imc.txt'

    try:
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()  # Remove espaços em branco e quebras de linha
                
                # Pula a linha se ela estiver vazia
                if not linha:
                    continue
                
                item = linha.split(';')
                
                # Verifica se a linha tem o número correto de elementos (5)
                if len(item) == 5:
                    imc_list.append({
                        'nome': item[0],
                        'peso': item[1],
                        'altura': item[2],
                        'imc': item[3],
                        'resultado': item[4]
                    })
    except FileNotFoundError:
        # Lida com o caso de o arquivo não existir
        return "Arquivo de dados não encontrado.", 404

    return render_template("consultar.html", prod=imc_list)

app.run(host='127.0.0.1', port=80, debug=True)
