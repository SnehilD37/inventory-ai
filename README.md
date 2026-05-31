# Smart Electronics Inventory AI Server

An AI-based inventory identification system that loads a custom-trained YOLOv8 object detection model (`best.pt`) on a local Flask server to identify smart electronic components. Detections are logged locally into a JSON database and returned as a JSON response, which can be viewed through a built-in interactive Web Dashboard.

---

## 📂 Project Structure

```text
IV_M/
├── app.py                 # Flask server (inference API + web dashboard)
├── best.pt                # Custom-trained YOLOv8 model (61 electronic classes)
├── test_images/           # Sample images for testing (Arduinos, sensors, motors, etc.)
├── test_client.py         # Python script to simulate and test API uploads
├── inventory_log.json     # JSON database for logged inventory detections
└── templates/
    └── dashboard.html     # HTML template for the premium web dashboard
```

---

## 🛠️ Setup & Installation

### Step 1: Install Python
Ensure you have **Python 3.10 or newer** installed. You can check your version in the terminal/command prompt:
```bash
python --version
```

### Step 2: Install Libraries
Install the required dependencies using `pip`:
```bash
pip install ultralytics flask opencv-python numpy requests
```

---

## 🚀 Running the Server

Start the Flask server by running the following command from the workspace directory:
```bash
python app.py
```

*Upon starting, the server will print the available model classes and begin listening on **port 5000**.*

---

## 🖥️ How to Use & Test

### 1. The Interactive Web Dashboard
Once the server is running, open your web browser and go to:
👉 **[http://localhost:5000/dashboard](http://localhost:5000/dashboard)**

From the dashboard, you can:
* **Drag-and-drop** any electronics image from the `test_images/` directory to run a prediction.
* View the predicted components, confidence scores, and raw JSON responses.
* See inventory scan metrics (Total scans, Unique components, Avg. confidence).
* Search and clear history logs.

### 2. Command Line Testing (API Client Simulation)
To simulate a request sent from a client (like an ESP32-CAM or a script) without using a browser, open a new terminal window and run:
```bash
python test_client.py <image_filename>
```
*Example:*
```bash
python test_client.py Arduino-Uno.jpg
```
This script will send a POST request with the image file to the `/predict` API and output the raw JSON response in the console.

### 3. Verify Server Status Route
Visiting **[http://localhost:5000](http://localhost:5000)** in the browser will return the plain text:
```text
Inventory AI Running
```

---

## 🌐 Network Access (Remote Deployment)

To allow other devices (like a phone, tablet, or ESP32-CAM) on the same Wi-Fi network to upload images:

1. Find your laptop's local IP address by running `ipconfig` (Windows) or `ifconfig` (Mac/Linux). Look for the IPv4 Address.
2. Make client HTTP POST requests directly to:
   ```text
   http://<YOUR_LAPTOP_IP>:5000/predict
   ```
3. Open the dashboard remotely from any device on your network using:
   ```text
   http://<YOUR_LAPTOP_IP>:5000/dashboard
   ```
