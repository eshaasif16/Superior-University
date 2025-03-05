import cv2
import numpy as np
import math

def detect_faces(image):
    """Detect faces in an image using Haar Cascade classifier."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load the face cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
  #detect fave
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    marked_image = image.copy()
    
    for (x, y, w, h) in faces:
        cv2.rectangle(marked_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return faces, marked_image

def analyze_face(image, face):
    """Analyze facial features to determine personality traits."""
    x, y, w, h = face
    
    #will extract face region for analysis
    face_region = image[y:y+h, x:x+w]
    gray_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
    
    #calculate face proportions
    face_width = w
    face_height = h
    aspect_ratio = face_width / face_height
    
    traits = {}
    
    # Face shape analysis
    if aspect_ratio > 0.85:
        traits["Face Shape"] = "Round or Square"
        traits["Potential Traits"] = "Friendly, approachable, and practical"
    else:
        traits["Face Shape"] = "Oval or Long"
        traits["Potential Traits"] = "Diplomatic, detail-oriented, and analytical"
    
    # Analyze brightness/darkness
    brightness = np.mean(gray_face)
    if brightness > 120:
        traits["Expression"] = "Bright/Open"
        traits["Communication Style"] = "Expressive and outgoing"
    else:
        traits["Expression"] = "Reserved/Serious"
        traits["Communication Style"] = "Thoughtful and introspective"
    
    # Symmetry analysis
    left_half = gray_face[:, :gray_face.shape[1]//2]
    right_half = gray_face[:, gray_face.shape[1]//2:]
    right_half_flipped = cv2.flip(right_half, 1)
    
    # resize if the halves have different shapes 
    if left_half.shape[1] != right_half_flipped.shape[1]:
        min_width = min(left_half.shape[1], right_half_flipped.shape[1])
        left_half = left_half[:, :min_width]
        right_half_flipped = right_half_flipped[:, :min_width]
    
    symmetry_diff = np.mean(cv2.absdiff(left_half, right_half_flipped))
    symmetry_score = 1 - (symmetry_diff / 255)
    
    if symmetry_score > 0.7:
        traits["Facial Symmetry"] = "High"
        traits["Decision Making"] = "Balanced and methodical"
    else:
        traits["Facial Symmetry"] = "Moderate"
        traits["Decision Making"] = "Creative and adaptable"
    #disclaimer 
    traits["Disclaimer"] = "This analysis is for entertainment purposes only and not based on scientific evidence."
    
    return traits