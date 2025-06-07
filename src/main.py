from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import random  # Для генерации примеров данных

app = Flask(__name__, static_folder='../static')
CORS(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_image(file_path):
    """Функция для анализа изображения (заглушка)"""
    # Здесь должна быть ваша реальная логика анализа изображения
    # Пока используем случайные данные для демонстрации
    
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Анализируем изображение
        analysis_results = analyze_image(file_path)
        
        return jsonify({
            'processed_image': f"/{file_path}",
            'classification': 'Vehicle',  # Основная классификация
            'analysis': analysis_results  # Детальная информация
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/get', methods=['GET'])
def get():
    return jsonify({'hello': 'hello'})

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8081)