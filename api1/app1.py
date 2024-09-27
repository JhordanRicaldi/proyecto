from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import io
import base64
import requests

app = Flask(__name__)
CORS(app)

# Función para preprocesar la imagen y convertir a base64
def load_and_preprocess_image(image):
    image = image.resize((224, 224))  # Cambia el tamaño a 224x224
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')  # Convertir a base64

@app.route('/predict', methods=['POST'])
def predict():
    print(request.files)  # Para depuración

    # Comprobar si el archivo está en la solicitud
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Verificar si el archivo es una imagen
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': 'File type not supported, please upload a PNG or JPG image'}), 400

    try:
        img = Image.open(io.BytesIO(file.read()))
    except Exception as e:
        return jsonify({'error': f'Error opening image: {str(e)}'}), 500
    
    # Preprocesar la imagen y convertir a base64
    processed_image = load_and_preprocess_image(img)

    # Reemplaza 'YOUR_HUGGING_FACE_TOKEN' con tu token de acceso real
    headers = {
        "Authorization": f"Bearer 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"
    }

    # Enviar la imagen a la API de Hugging Face
    response = requests.post(
        "https://api-inference.huggingface.co/models/Jhordan12345/food-nutrition-predictor",
        headers=headers,  # Añadir las cabeceras con el token
        json={"inputs": processed_image}  # Enviar como base64
    )
    
    if response.status_code != 200:
        return jsonify({'error': f'Error en la predicción: {response.text}'}), 500  # Devuelve el mensaje de error

    # Procesar la respuesta de la API
    prediction = response.json()

    # Ajusta esta parte según el formato real de la respuesta
    try:
        proteins, carbs, fats = prediction['predictions'][0]  # Asegúrate de que esta parte sea correcta
    except (KeyError, IndexError) as e:
        return jsonify({'error': 'Error al obtener predicciones'}), 500

    return jsonify({
        'proteins': float(proteins),
        'carbs': float(carbs),
        'fats': float(fats)
    })

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'description': 'Esta API predice el valor nutricional de platos de comida a partir de imágenes.',
        'endpoints': {
            '/predict': {
                'method': 'POST',
                'description': 'Envía una imagen de un plato de comida para recibir una predicción de proteínas, carbohidratos y grasas.',
                'params': {
                    'file': 'La imagen del plato (formato permitido: jpg, png)'
                }
            }
        },
        'note': 'Asegúrate de que el modelo esté cargado y en funcionamiento.'
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5005)
