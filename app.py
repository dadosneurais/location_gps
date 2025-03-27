from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime as dt, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'key'

# connect
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    db = client["db_locations"]
    logs_collection = db["logs"]
    
    print("✅ Connected!")

except Exception as e:
    print(f"❌ Error {e}")
    exit(1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.json

    timestamp = (dt.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    
    ip = request.remote_addr

    log_data = {
        "ip": ip,
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "timestamp": timestamp
    }

    # commit
    logs_collection.insert_one(log_data)

    return jsonify({"message": "Localização salva!", "data": log_data}), 201

if __name__ == '__main__':
    app.run(debug=False)
