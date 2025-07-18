from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

app = Flask(__name__)

# Basic configurations

# Fetch MongoDB URI from environment variable
app.config["MONGO_URI"] =os.environ.get("MONGO_URI")


# CORS setup
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

mongo = PyMongo(app)

@app.route('/')
def about():
    return render_template('index.html')

@app.route('/write_diary')
def write_diary():
    return render_template('write_diary.html')

@app.route('/diaries_page')
def diaries_page():
    return render_template('diaries.html')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Save diary entry
@app.route('/diary', methods=['POST'])
def save_diary():
    try:
        diaries = mongo.db.diaries  # This will create the 'diaries' collection automatically when inserting data
        content = request.json.get('content')
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        diaries.insert_one({'content': content})
        return jsonify({'message': 'Diary saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get diary entries
@app.route('/diaries', methods=['GET'])
def get_diaries():
    try:
        diaries = mongo.db.diaries  # Reference to 'diaries' collection
        if diaries.count_documents({}) == 0:
            return jsonify({'message': 'No diaries found.'})
        all_diaries = list(diaries.find())
        return jsonify([{'content': diary['content']} for diary in all_diaries])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5003, debug=True)
