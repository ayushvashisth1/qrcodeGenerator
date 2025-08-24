# app.py
from flask import Flask, render_template, request, jsonify
import qrcode
from io import BytesIO
import base64

# Initialize the Flask application
app = Flask(__name__)

# Route to serve the main HTML page
@app.route('/')
def index():
    """
    Serves the main HTML page of the QR Code Generator.
    """
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    """
    Generates a QR code from a URL received in a POST request.
    The QR code image is returned as a base64-encoded string.
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL not provided'}), 400

        url = data['url']

        # Create a QR code instance
        qr_image = qrcode.make(url)
        
        # Save the QR code image to a byte stream
        img_bytes_stream = BytesIO()
        qr_image.save(img_bytes_stream, format='PNG')
        img_bytes_stream.seek(0)

        # Encode the image bytes to a base64 string
        base64_image = base64.b64encode(img_bytes_stream.read()).decode('utf-8')

        # Return the base64 string in a JSON response
        return jsonify({'image': base64_image})

    except Exception as e:
        print(f"Error generating QR code: {e}")
        return jsonify({'error': 'Failed to generate QR code'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
