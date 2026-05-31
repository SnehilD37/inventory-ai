import os
import sys
import requests
import json

# Configuration
SERVER_URL = "http://localhost:5000/predict"
IMAGE_DIR = "test_images"

def test_prediction(image_name):
    image_path = os.path.join(IMAGE_DIR, image_name)
    if not os.path.exists(image_path):
        print(f"Error: Test image not found at {image_path}")
        return False
        
    print(f"\n--- Testing API Endpoint: POST {SERVER_URL} ---")
    print(f"Uploading file: {image_name}...")
    
    try:
        with open(image_path, 'rb') as img_file:
            files = {'image': (image_name, img_file, 'image/jpeg')}
            response = requests.post(SERVER_URL, files=files)
            
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            predictions = response.json()
            print("\nResponse Body (JSON):")
            print(json.dumps(predictions, indent=2))
            
            if predictions:
                print("\nIdentification Result:")
                for pred in predictions:
                    print(f"  • Component: {pred['component']} (Confidence: {pred['confidence'] * 100:.1f}%)")
            else:
                print("\nResult: No components detected in the image.")
            return True
        else:
            print("Error Response:")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the Flask server.")
        print("Please verify the server is running by executing: python app.py")
        return False
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return False

def show_available_images():
    if not os.path.exists(IMAGE_DIR):
        print(f"Error: {IMAGE_DIR} folder does not exist.")
        return []
    
    # Filter files that end with typical image extensions
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return sorted(images)

if __name__ == "__main__":
    available_images = show_available_images()
    
    if not available_images:
        print("No test images found in the 'test_images' directory.")
        sys.exit(1)
        
    # Check if a custom file was passed as argument
    if len(sys.argv) > 1:
        target_image = sys.argv[1]
        # Resolve path
        if not target_image.startswith(IMAGE_DIR):
            target_image_name = os.path.basename(target_image)
        else:
            target_image_name = target_image
    else:
        # Default to a few popular components if available, otherwise pick the first image
        presets = ["Arduino-Uno.jpg", "Servo-Motor.jpg", "ESP32.jpg"]
        target_image_name = None
        for p in presets:
            if p in available_images:
                target_image_name = p
                break
        
        if not target_image_name:
            target_image_name = available_images[0]
            
    print(f"Available test images in '{IMAGE_DIR}/':")
    for idx, img in enumerate(available_images[:10]):
        print(f"  {idx + 1}. {img}")
    if len(available_images) > 10:
        print(f"  ... and {len(available_images) - 10} more.")
        
    print(f"\nDefaulting test image to: {target_image_name}")
    print("To test a different image, run: python test_client.py <image_filename>")
    
    test_prediction(target_image_name)
