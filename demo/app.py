import gradio as gr
import numpy as np
from huggingface_hub import hf_hub_download
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import time
import shutil

# Descargar el modelo desde Hugging Face
repo_id = "Jhordan12345/food-predictor"  # Reemplázalo por tu usuario y repo

# Maximum number of download attempts
max_attempts = 5
# Delay between download attempts in seconds
retry_delay = 10

for attempt in range(max_attempts):
    try:
        # Delete the cached file if it exists, including the directory
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
        repo_cache_dir = os.path.join(cache_dir, repo_id.split("/")[0], repo_id.split("/")[1])

        if os.path.exists(repo_cache_dir):
            shutil.rmtree(repo_cache_dir)
            print(f"Deleted cached directory: {repo_cache_dir}")

        # Force the download to avoid using cached files
        model_file = hf_hub_download(repo_id=repo_id, filename="modelo_alimentos.h5", force_download=True)
        model = load_model(model_file)

        break
    except OSError as e:
        print(f"Download attempt {attempt + 1} failed: {e}")
        if attempt < max_attempts - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            raise  # Re-raise the exception if all attempts fail

# Función para preprocesar la imagen y hacer predicciones
def predict_image(img):
    img = img.resize((224, 224))  # Cambiar el tamaño de la imagen
    img_array = image.img_to_array(img) / 255.0  # Normalizar
    img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión para el batch
    prediction = model.predict(img_array)
    return {
        "Proteínas (g)": prediction[0][0],
        "Carbohidratos (g)": prediction[0][1],
        "Grasas (g)": prediction[0][2]
    }

# Crear la interfaz en Gradio
interface = gr.Interface(
    fn=predict_image,
    inputs=gr.Image(type="pil"),  # Entrada: Imagen
    outputs=[
        gr.Label(num_top_classes=3)  # Salida: Predicción de proteínas, carbohidratos, grasas
    ],
    title="Análisis Nutricional de Platos de Comida",
    description="Sube una imagen de tu plato y obtén una predicción de proteínas, carbohidratos y grasas."
)

# Iniciar la interfaz
interface.launch()