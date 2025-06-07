import os
from flask import Flask, request, jsonify
import torch
import torchvision.transforms as transforms
from PIL import Image
from model import GestureCNN
from utils import extract_frames


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the trained model
model = GestureCNN(num_classes=4)
model.load_state_dict(torch.load('gesture_model.pth', map_location=torch.device('cpu')))
model.eval()

# Define transformation for input frames
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

gesture_labels = ['swipe left', 'swipe right', 'swipe up', 'swipe down']

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    print(f"[INFO] Uploaded video saved to: {filepath}")
    return jsonify({'message': 'Video uploaded successfully', 'filename': file.filename}), 200

@app.route('/predict', methods=['GET'])
def predict():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return jsonify({'error': 'No video found. Please upload first.'}), 400
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], files[-1])  # Use the most recent upload
    print(f"[INFO] Running inference on: {video_path}")

    frames = extract_frames(video_path)
    if not frames:
        return jsonify({'error': 'No frames extracted'}), 500

    predictions = []
    for frame in frames:
        image = transform(frame).unsqueeze(0)  # Add batch dimension
        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)
            predictions.append(predicted.item())

    # Majority vote
    final_pred = max(set(predictions), key=predictions.count)
    gesture = gesture_labels[final_pred]

    return jsonify({'gesture': gesture}), 200

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1', help='Host to run server on (use 0.0.0.0 for public)')
    parser.add_argument('--port', default=5000, type=int, help='Port to run server on')
    args = parser.parse_args()

    print(f"[INFO] Starting Flask server at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port)
