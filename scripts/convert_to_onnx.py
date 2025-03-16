import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Вимкнути oneDNN попередження

import warnings
import tensorflow as tf
import tf2onnx

def convert_to_onnx():
    # Вимкнути специфічні попередження TensorFlow
    warnings.filterwarnings("ignore", category=UserWarning, module="tensorflow")

    # Завантажити модель
    model_path = "models/ui_classifier_v2.h5"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Модель {model_path} не знайдено!")
    
    model = tf.keras.models.load_model(model_path)
    
    # Явно вказати output_names для Sequential
    if isinstance(model, tf.keras.Sequential):
        model.output_names = [f"output_{i}" for i in range(len(model.outputs))]
        if model.input_shape is None:
            model.build(input_shape=(None, 64, 64, 3))  # Форма з 2_train_model.py
    
    # Вхідна сигнатура (64x64x3!)
    input_signature = [tf.TensorSpec(shape=(None, 64, 64, 3), dtype=tf.float32)]
    
    # Конвертація з ігноруванням застарілих попереджень
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        onnx_model, _ = tf2onnx.convert.from_keras(
            model, 
            input_signature=input_signature, 
            opset=13
        )
    
    # Зберегти ONNX
    output_path = "models/ui_classifier.onnx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(onnx_model.SerializeToString())
    
    print(f"✅ Модель конвертована у {output_path}!")

if __name__ == "__main__":
    convert_to_onnx()