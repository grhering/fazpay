from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

TAXAS = {
    "Débito": {"Visa/Master": 2.29, "Demais Bandeiras": 2.75},
    "Crédito à vista": {"Visa/Master": 5.78, "Demais Bandeiras": 6.24},
    "Crédito parcelado em 2x": {"Visa/Master": 6.99, "Demais Bandeiras": 7.49},
    "Crédito parcelado em 3x": {"Visa/Master": 7.61, "Demais Bandeiras": 8.12},
    "Crédito parcelado em 4x": {"Visa/Master": 8.28, "Demais Bandeiras": 8.78},
    "Crédito parcelado em 5x": {"Visa/Master": 8.8, "Demais Bandeiras": 9.34},
    "Crédito parcelado em 6x": {"Visa/Master": 9.65, "Demais Bandeiras": 10.13},
    "Crédito parcelado em 7x": {"Visa/Master": 10.9, "Demais Bandeiras": 11.58},
    "Crédito parcelado em 8x": {"Visa/Master": 11.79, "Demais Bandeiras": 12.45},
    "Crédito parcelado em 9x": {"Visa/Master": 12.48, "Demais Bandeiras": 13.18},
    "Crédito parcelado em 10x": {"Visa/Master": 13.18, "Demais Bandeiras": 13.82},
    "Crédito parcelado em 11x": {"Visa/Master": 13.76, "Demais Bandeiras": 14.56},
    "Crédito parcelado em 12x": {"Visa/Master": 14.78, "Demais Bandeiras": 15.31},
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora de Taxas</title>
</head>
<body>
    <h1>Calculadora de Valor Recebido</h1>
    <form method="POST">
        <label>Valor total (R$):</label>
        <input type="number" name="valor" step="0.01" required><br><br>

        <label>Bandeira:</label>
        <select name="bandeira">
            <option value="Visa/Master">Visa/Master</option>
            <option value="Demais Bandeiras">Demais Bandeiras</option>
        </select><br><br>

        <label>Forma de pagamento:</label>
        <select name="forma_pagamento">
            {% for forma in formas_pagamento %}
                <option value="{{ forma }}">{{ forma }}</option>
            {% endfor %}
        </select><br><br>

        <input type="submit" value="Calcular">
    </form>

    {% if resultado is not none %}
        <h2>Você receberá: R$ {{ resultado }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        valor_total = float(request.form['valor'])
        bandeira = request.form['bandeira']
        forma_pagamento = request.form['forma_pagamento']
        taxa = TAXAS[forma_pagamento][bandeira]
        resultado = round(valor_total * (1 - taxa / 100), 2)

    return render_template_string(HTML_TEMPLATE, resultado=resultado, formas_pagamento=TAXAS.keys())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
