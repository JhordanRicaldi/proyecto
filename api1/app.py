from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import h5py

app = Flask(__name__)
CORS(app)

# Función para cargar el modelo en dos partes
def load_model_in_parts():
    model = tf.keras.models.Model()
    with h5py.File('modelo_alimentos_parte1.h5', 'r') as f1, h5py.File('modelo_alimentos_parte2.h5', 'r') as f2:
        for key in f1.keys():
            weight = f1[key][:]
            model.add(tf.keras.layers.Dense(weight.shape[1], input_shape=(weight.shape[0],)))
            model.layers[-1].set_weights([weight])
        for key in f2.keys():
            weight = f2[key][:]
            model.add(tf.keras.layers.Dense(weight.shape[1]))
            model.layers[-1].set_weights([weight])
    return model

# Cargar el modelo
model = load_model_in_parts()

# El resto de tu código permanece igual
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
    app.run(debug=True, host='127.0.0.1', port=5001)