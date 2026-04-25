from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return "TaskMile API is Active!"

@app.route('/get-pairing-code', methods=['GET'])
def pairing_code():
    phone_number = request.args.get('number')
    if not phone_number:
        return jsonify({"error": "Number missing"}), 400
    if not phone_number.startswith('92'):
        phone_number = '92' + phone_number.lstrip('0')
    try:
        script_path = os.path.join(BASE_DIR, 'server.js')
        result = subprocess.run(
            ['node', script_path, phone_number], 
            capture_output=True, text=True, timeout=50
        )
        code = result.stdout.strip()
        return jsonify({"code": code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
