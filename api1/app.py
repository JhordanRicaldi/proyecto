from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Cargar el modelo previamente entrenado
model = tf.keras.models.load_model('modelo_alimentos.h5')

# Función para procesar la imagen
def load_and_preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    img = Image.open(io.BytesIO(file.read()))
    
    processed_image = load_and_preprocess_image(img)
    prediction = model.predict(processed_image)
    
    proteins, carbs, fats = prediction[0]
    
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
    app.run(debug=True, host='127.0.0.1', port=5001)  # Puedes cambiar "5001" por el puerto que prefieras

