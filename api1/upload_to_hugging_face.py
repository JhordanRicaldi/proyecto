# import tensorflow as tf
# from transformers import TFAutoModel, AutoConfig
# from huggingface_hub import push_to_hub

# def prepare_model_for_huggingface(model_path):
#     # Cargar tu modelo
#     model = tf.keras.models.load_model(model_path)
    
#     # Crear una configuración para el modelo
#     config = AutoConfig.from_pretrained("bert-base-uncased")
#     config.architectures = ["TFCustomModel"]
#     # Ajusta este número según las salidas de tu modelo (proteínas, carbohidratos, grasas)
#     config.num_labels = 3
#     config.hidden_size = model.layers[-1].output_shape[-1]
    
#     # Crear un modelo compatible con Hugging Face
#     hf_model = TFAutoModel.from_config(config)
    
#     # Copiar los pesos de tu modelo al modelo de Hugging Face
#     for i, layer in enumerate(model.layers):
#         hf_model.layers[i].set_weights(layer.get_weights())
    
#     return hf_model

# def upload_to_huggingface(hf_model, repo_name):
#     push_to_hub(
#         model=hf_model,
#         repo_id=f"Jhordan12345/{repo_name}",
#         use_auth_token="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"
#     )

# if __name__ == "__main__":
#     # Preparar el modelo
#     hf_model = prepare_model_for_huggingface("modelo_alimentos.h5")
    
#     # Subir el modelo
#     upload_to_huggingface(hf_model, "food-nutrition-predictor")  # Puedes cambiar "food-nutrition-predictor" si deseas un nombre diferente para tu repositorio

# print("Modelo subido exitosamente a Hugging Face!")

from huggingface_hub import HfApi

api = HfApi()
api.upload_file(
    path_or_fileobj="modelo_alimentos.h5",
    path_in_repo="modelo_alimentos.h5",
    repo_id="Jhordan12345",
    token="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"
)
