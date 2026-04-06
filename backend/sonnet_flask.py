from flask import Flask, request, jsonify
from flask_cors import CORS
import sonnet_invoke
import base64
import os

app = Flask(__name__)
CORS(app)

# Folder to store uploaded screenshots
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# This will hold the path to the most recent uploaded screenshot
LATEST_IMAGE_PATH = os.path.join(UPLOAD_FOLDER, 'latest.png')

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Accepts a base64 image from the frontend and saves it as 'latest.png'
    """
    data = request.get_json()
    image_data = data.get('image_data')
    filename = data.get('filename', 'latest.png')

    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        image_bytes = base64.b64decode(image_data)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        # Update the global latest image path (optional)
        global LATEST_IMAGE_PATH
        LATEST_IMAGE_PATH = filepath

        return jsonify({'message': 'Image saved', 'path': filepath}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output', methods=['GET'])
def get_model_output():
    """
    Runs AI analysis on the most recently uploaded image.
    """
    if not os.path.exists(LATEST_IMAGE_PATH):
        return jsonify({'error': 'No uploaded image found'}), 404

    print(f"Analyzing image: {LATEST_IMAGE_PATH}")
    result = sonnet_invoke.get_model_output(LATEST_IMAGE_PATH)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)