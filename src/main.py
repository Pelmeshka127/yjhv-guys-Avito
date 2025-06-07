from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='../static')
CORS(app)  # Разрешаем CORS для всех доменов (для разработки)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        
        image_url = f"/{file_path}"
        
        return jsonify({
            'processed_image': image_url,
            'classification': 'Image uploaded successfully'
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/get', methods=['GET'])
def get():
    return jsonify({'hello': 'hello'})  # Исправлено здесь

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8081)