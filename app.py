from flask import Flask, render_template, request, redirect, url_for, flash
from qr_utils import generate_qr, validate_qr
import json
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'
QR_FOLDER = 'static/qrcodes'

if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    user_id = request.form['user_id']
    
    if name and user_id:
        qr_filename = generate_qr(name, user_id)
        
        # Guardar en base de datos local (archivo json)
        with open('database.json', 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append({'name': name, 'user_id': user_id})
            f.seek(0)
            json.dump(data, f, indent=4)

        flash('Código QR generado correctamente.')
        return redirect(url_for('index'))
    else:
        flash('Faltan datos.')
        return redirect(url_for('index'))

@app.route('/validate', methods=['POST'])
def validate():
    scanned_code = request.form['scanned_code']
    if validate_qr(scanned_code):
        flash('Acceso permitido.')
    else:
        flash('Acceso denegado.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
