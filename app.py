from flask import Flask, request, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

def calcular_parcelas(valor_total, parcelas, dia_vencimento):
    if parcelas > 4:
        parcelas = 4

    entrada = valor_total * 0.5
    valor_parcela = (valor_total - entrada) / parcelas

    if valor_parcela < 35:
        return None

    data_atual = datetime.now()
    data_entrada = (data_atual + timedelta(days=3)).strftime("%d/%m/%Y")

    # Calcular o mês e ano da primeira parcela com base na entrada e no dia de vencimento
    dia_vencimento = int(dia_vencimento)
    mes_vencimento = data_atual.month
    ano_vencimento = data_atual.year
    if data_atual.day > dia_vencimento:
        mes_vencimento += 1
        if mes_vencimento > 12:
            mes_vencimento = 1
            ano_vencimento += 1
    data_parcelas = [datetime(ano_vencimento, mes_vencimento, dia_vencimento)]

    for i in range(parcelas - 1):
        mes_vencimento += 1
        if mes_vencimento > 12:
            mes_vencimento = 1
            ano_vencimento += 1
        data_parcelas.append(datetime(ano_vencimento, mes_vencimento, dia_vencimento))

    data_parcelas = [data.strftime("%d/%m/%Y") for data in data_parcelas]

    texto = f"""#ACORDO REALIZADO DAS FATURAS DOS DIAS (, )

VALOR TOTAL NEGOCIADO: R$ {valor_total:.2f}
ENTRADA: R${entrada:.2f}

"""

    if parcelas == 1:
        texto += f"PARCELADO DE 1 VEZ,\n"
        texto += f"SENDO UMA ENTRADA DE R${entrada:.2f}.\n\n"
    else:
        texto += f"PARCELADO DE {parcelas} VEZES,\n"
        texto += f"SENDO UMA ENTRADA DE R${entrada:.2f} E {parcelas} PARCELAS DE R${valor_parcela:.2f}.\n\n"

    texto += "BOLETOS GERADOS COM NOVOS VENCIMENTOS:\n"
    texto += "(descrever data de vencimento das parcelas do acordo e entrada):\n\n"

    texto += f"ENTRADA: {data_entrada}\n"

    for i in range(1, parcelas + 1):
        texto += f"PARCELA{i}: {data_parcelas[i-1]}\n"

    return texto

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        valor_total = float(request.form['valor_total'].replace(",", "."))
        parcelas = int(request.form['parcelas'])
        data_entrada = datetime.strptime(request.form['vencimento'], "%Y-%m-%d")

        resultado = calcular_parcelas(valor_total, parcelas, data_entrada)
        if resultado is not None:
            entrada, valor_parcela, data_parcelas = resultado
            return render_template('resultados.html', valor_total=valor_total, entrada=entrada, parcelas=parcelas, valor_parcela=valor_parcela, data_entrada=data_entrada, data_parcelas=data_parcelas)

    return render_template('index.html')  # Não precisa mais do prefixo 'templates/'

    app.run(debug=True)
