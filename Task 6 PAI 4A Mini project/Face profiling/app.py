from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def analyze_face(image_path):
    try:
        # will read the image 
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Load the face cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            return None
        
        # Get the first face
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        
        avg_brightness = np.mean(face_roi) / 255.0
        contrast = np.std(face_roi) / 255.0
        symmetry = calculate_symmetry(face_roi)
        
        #for traits
        traits = {
            "Openness": min(max(avg_brightness * 0.7 + contrast * 0.3, 0), 1),
            "Conscientiousness": min(max(symmetry * 0.8 + contrast * 0.2, 0), 1),
            "Extraversion": min(max(avg_brightness * 0.6 + contrast * 0.4, 0), 1),
            "Agreeableness": min(max(symmetry * 0.6 + avg_brightness * 0.4, 0), 1),
            "Neuroticism": min(max(contrast * 0.7 + (1 - symmetry) * 0.3, 0), 1)
        }
        
        return traits
        
    except Exception as e:
        print(f"Error in analyze_face: {str(e)}")
        return None

def calculate_symmetry(face_roi):
    # basic symmetry score calculations
    height, width = face_roi.shape
    mid = width // 2
    left_side = face_roi[:, :mid]
    right_side = face_roi[:, mid:width]
    right_side_flipped = cv2.flip(right_side, 1)
    
    # Resize if the sides have different shapes
    if left_side.shape != right_side_flipped.shape:
        min_width = min(left_side.shape[1], right_side_flipped.shape[1])
        left_side = left_side[:, :min_width]
        right_side_flipped = right_side_flipped[:, :min_width]
    
    # Calculate symmetry score
    diff = np.abs(left_side.astype(float) - right_side_flipped.astype(float))
    symmetry_score = 1 - (np.mean(diff) / 255.0)
    
    return symmetry_score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    try:
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        #facial analysis
        traits = analyze_face(filepath)
        
        if traits is None:
            return jsonify({'error': 'No face detected in the image'}), 400
        
        return jsonify({
            'traits': traits,
            'image_path': f'/static/uploads/{filename}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)