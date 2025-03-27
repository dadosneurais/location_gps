from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime as dt
import os
import requests
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'key'

# Conectar ao MongoDB
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["db_locations"]
    logs_collection = db["logs"]
    
    # Criar coleção se não existir
    if "logs" not in db.list_collection_names():
        db.create_collection("logs")

    print("✅ Conexão com MongoDB estabelecida!")

except Exception as e:
    print(f"❌ Erro ao conectar ao MongoDB: {e}")
    exit(1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/salvar_localizacao', methods=['POST'])
def salvar_localizacao():
    data = request.json
    
    if not data or "latitude" not in data or "longitude" not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    ip = request.remote_addr

    log_data = {
        "ip": ip,
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "timestamp": dt.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Salvar no MongoDB
    logs_collection.insert_one(log_data)

    return jsonify({"message": "Localização salva!", "data": log_data}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
