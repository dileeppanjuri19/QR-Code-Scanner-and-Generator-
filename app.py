from flask import Flask, render_template, request, jsonify
import qrcode
import io
import base64
from pyzbar.pyzbar import decode
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.json.get('data', '')
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    qr = qrcode.make(data)
    buf = io.BytesIO()
    qr.save(buf, 'PNG')
    img_bytes = buf.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('ascii')
    return jsonify({'image': img_base64})

@app.route('/scan', methods=['POST'])
def scan_qr():
    image_data = request.files.get('image')
    if not image_data:
        return jsonify({'error': 'No image uploaded'}), 400

    image = Image.open(image_data.stream)
    decoded_objs = decode(image)

    if decoded_objs:
        result = decoded_objs[0].data.decode('utf-8')
        return jsonify({'result': result})
    else:
        return jsonify({'result': 'No QR code found'})

if __name__ == '__main__':
    app.run(debug=True)