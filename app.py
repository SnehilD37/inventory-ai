import os
import json
import datetime
from flask import Flask, request, jsonify, render_template
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

# Ensure best.pt exists
MODEL_PATH = 'best.pt'
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file {MODEL_PATH} not found in the current directory.")

# Load the model
print("Loading YOLO model...")
model = YOLO(MODEL_PATH)
print("Model loaded successfully.")
print("Model classes available:")
print(model.names)

# Logging file path
LOG_FILE = 'inventory_log.json'

def log_detection(component, confidence):
    """Logs the detected component with confidence score and timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = {
        "component": component,
        "confidence": round(float(confidence), 2),
        "timestamp": timestamp
    }
    
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
            if not isinstance(logs, list):
                logs = []
        except Exception:
            logs = []
            
    # Prepend to show the latest detections first
    logs.insert(0, new_entry)
    
    try:
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Error writing to log file: {e}")

@app.route('/')
def home():
    # Returns Inventory AI Running as requested in Task 2.1
    return "Inventory AI Running"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logs', methods=['GET'])
def get_logs():
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except Exception:
            pass
    return jsonify(logs)

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    try:
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image key in form data"}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    try:
        # Read image using OpenCV
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "Invalid image format"}), 400
            
        # Run YOLOv8 inference
        results = model(img)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                # Normalize spaces to hyphens for conformity (e.g., "Arduino Uno" -> "Arduino-Uno")
                raw_name = model.names[class_id]
                class_name = raw_name.replace(" ", "-")
                
                confidence = float(box.conf[0])
                
                detections.append({
                    "component": class_name,
                    "confidence": round(confidence, 2)
                })
                
                # Log detection to database
                log_detection(class_name, confidence)
                
        # Return response
        return jsonify(detections)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Listen on 0.0.0.0 and port 5000 as required in Task 3.1
    # Use debug=False to avoid loading model twice in Flask reloader
    app.run(host='0.0.0.0', port=5000, debug=False)
