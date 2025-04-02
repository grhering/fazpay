from flask import Flask, render_template_string, request, send_from_directory
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
<html lang='pt-br'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script>
        function toggleModo() {
            const normal = document.getElementById('modo-normal');
            const reverso = document.getElementById('modo-reverso');
            if (normal.style.display === 'none') {
                normal.style.display = 'block';
                reverso.style.display = 'none';
            } else {
                normal.style.display = 'none';
                reverso.style.display = 'block';
            }
        }
    </script>
    <title>Calculadora de Taxas - FAZPAY</title>
</head>
<body class="bg-light">
    <div class="container py-4">
        <div class="text-center mb-4">
            <img src="/logo" alt="Fazpay Logo" height="60">
            <h2 class="mt-2">Calculadora de Taxas</h2>
            <p class="text-muted">Simule quanto você vai receber ou quanto precisa passar</p>
        </div>
        <div class="card mx-auto shadow p-4" style="max-width: 500px;">
            <button onclick="toggleModo()" class="btn btn-outline-secondary mb-3">🔁 Alternar modo</button>
            <form method="POST">
                <input type="hidden" name="modo" value="normal" id="modo-escolhido">
                <div id="modo-normal">
                    <div class="mb-3">
                        <label class="form-label">Valor total (R$)</label>
                        <input type="number" name="valor" step="0.01" class="form-control">
                    </div>
                </div>
                <div id="modo-reverso" style="display: none;">
                    <div class="mb-3">
                        <label class="form-label">Quero receber (R$)</label>
                        <input type="number" name="valor_desejado" step="0.01" class="form-control">
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Bandeira</label>
                    <select name="bandeira" class="form-select">
                        <option value="Visa/Master">Visa/Master</option>
                        <option value="Demais Bandeiras">Demais Bandeiras</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">Forma de pagamento</label>
                    <select name="forma_pagamento" class="form-select">
                        {% for forma in formas_pagamento %}
                            <option value="{{ forma }}">{{ forma }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="d-grid">
                    <button type="submit" class="btn btn-primary">Calcular</button>
                </div>
            </form>
            {% if resultado is not none %}
                <div class="alert alert-success mt-4 text-center">
                    {% if modo == 'normal' %}
                        <h5>Valor original: <strong>R$ {{ valor_total }}</strong></h5>
                        <h5>Você receberá: <strong>R$ {{ resultado }}</strong></h5>
                    {% else %}
                        <h5>Você quer receber: <strong>R$ {{ valor_desejado }}</strong></h5>
                        <h5>Você deve passar: <strong>R$ {{ resultado }}</strong></h5>
                    {% endif %}
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    valor_total = None
    valor_desejado = None
    modo = 'normal'
    if request.method == 'POST':
        bandeira = request.form['bandeira']
        forma_pagamento = request.form['forma_pagamento']
        taxa = TAXAS[forma_pagamento][bandeira]
        modo = request.form.get('modo', 'normal')

        if 'valor' in request.form and request.form['valor']:
            valor_total = float(request.form['valor'])
            resultado = round(valor_total * (1 - taxa / 100), 2)
        elif 'valor_desejado' in request.form and request.form['valor_desejado']:
            valor_desejado = float(request.form['valor_desejado'])
            resultado = round(valor_desejado / (1 - taxa / 100), 2)
            modo = 'reverso'

    return render_template_string(HTML_TEMPLATE, resultado=resultado, valor_total=valor_total, valor_desejado=valor_desejado, modo=modo, formas_pagamento=TAXAS.keys())

@app.route('/logo')
def logo():
    return send_from_directory('.', 'image.png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
