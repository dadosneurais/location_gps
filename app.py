from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime as dt, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["db_locations"]
logs_collection = db["logs"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    if not data or "latitude" not in data or "longitude" not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    log_data = {
        "ip": request.remote_addr,
        "gps": [data["latitude"], data["longitude"]],
        "timestamp": (dt.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    }

    logs_collection.insert_one(log_data)
    return jsonify({"message": "Localização salva!", "data": log_data}), 201

if __name__ == '__main__':
    app.run(debug=False)
