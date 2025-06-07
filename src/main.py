from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import random
import uuid

import hashlib

# Замена uuid.uuid4().hex на хэш содержимого файла
def generate_filename_hash(file_content):
    hash_obj = hashlib.sha256(file_content)
    return hash_obj.hexdigest()  # уникальный хэш на основе содержимого файла

app = Flask(__name__, static_folder='../static')
CORS(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_images(file_paths):
    """Функция для анализа набора изображений (заглушка)"""
    # Здесь должна быть ваша реальная логика анализа всех изображений вместе
    # Генерируем общее описание для всех фотографий
    
    makes = ['Toyota', 'Honda', 'BMW', 'Mercedes', 'Audi', 'Ford']
    models = ['Camry', 'Civic', 'X5', 'E-Class', 'A4', 'Focus']
    years = list(range(2010, 2023))
    colors = ['Red', 'Blue', 'Black', 'White', 'Silver', 'Gray']
    conditions = ['Excellent', 'Good', 'Fair', 'Needs repair']
    
    return {
        'make': random.choice(makes),
        'model': random.choice(models),
        'year': random.choice(years),
        'color': random.choice(colors),
        'condition': random.choice(conditions),
        'price_range': f"${random.randint(5000, 30000)}-${random.randint(30000, 80000)}",
        'features': random.sample([
            'Leather seats', 'Sunroof', 'Navigation', 
            'Backup camera', 'Bluetooth', 'Heated seats'
        ], k=3),
        'market_analysis': f"Similar cars in your area are priced {random.randint(10, 30)}% higher than average."
    }

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part'}), 400
    
    files = request.files.getlist('files')
    
    if len(files) == 0:
        return jsonify({'error': 'No selected files'}), 400
    
    saved_files = []
    
    # Сохраняем все файлы
    for file in files:
        if file.filename == '':
            continue
            
        if not (file and allowed_file(file.filename)):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Генерируем уникальное имя файла
        unique_filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        saved_files.append(file_path)
    
    # Анализируем все изображения вместе
    common_analysis = analyze_images(saved_files)
    
    # Формируем ответ с общим анализом и списком изображений
    images_data = []
    for file_path in saved_files:
        images_data.append({
            'processed_image': f"/{file_path}",
            'classification': 'Vehicle'
        })
    
    return jsonify({
        'common_analysis': common_analysis,
        'images': images_data
    })

@app.route('/get', methods=['GET'])
def get():
    return jsonify({'hello': 'hello'})

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8081)