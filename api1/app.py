from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client, handle_file
import tempfile

app = Flask(__name__)
CORS(app)

# Ruta del modelo en Hugging Face
MODEL_NAME = "Jhordan12345/food-predictor"

# Crear una instancia del cliente
client = Client(MODEL_NAME)

def call_hugging_face_api(image):
    # Guardar el archivo en una ubicación temporal
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    image.save(temp_file.name)

    # Llamar a la función handle_file con la ruta del archivo temporal
    result = client.predict(img=handle_file(temp_file.name), api_name="/predict")
    return result

@app.route('/predict', methods=['POST'])
def predict():
    # Obtener la imagen de la solicitud
    image = request.files['file']

    # Llamar a la API de Hugging Face
    result = call_hugging_face_api(image)

    # Procesar el resultado
    if result is not None:
        # Ajustar esta parte según el formato real de la respuesta
        try:
            # Suponiendo que la respuesta es un diccionario con las claves correspondientes
            proteins = result.get('Proteínas (g)', 0)
            carbs = result.get('Carbohidratos (g)', 0)
            fats = result.get('Grasas (g)', 0)

            return jsonify({
                'proteins': float(proteins),
                "carbs": float(carbs),
                'fats': float(fats)
            })
        except (ValueError, TypeError) as e:
            return jsonify({'error': 'Error al procesar los valores de predicción'}), 500
    else:
        return jsonify({'error': 'Error en la predicción'}), 500

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
