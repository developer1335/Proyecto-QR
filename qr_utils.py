import qrcode
import os
import json

def generate_qr(name, user_id):
    data = f"{name}-{user_id}"
    img = qrcode.make(data)
    filename = f"{user_id}.png"
    path = os.path.join('static/qrcodes', filename)
    img.save(path)
    return filename

def validate_qr(code):
    try:
        with open('database.json', 'r') as f:
            data = json.load(f)
            return any(f"{entry['name']}-{entry['user_id']}" == code for entry in data)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
