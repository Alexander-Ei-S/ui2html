# scripts/onnx_inference.py
import onnxruntime as ort
import numpy as np
from PIL import Image
import os

def predict(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл {image_path} не знайдено!")
    
    try:
        # Використовуємо правильний провайдер для AMD GPU
        session = ort.InferenceSession(
            "models/ui_classifier.onnx",
            providers=['DmlExecutionProvider', 'CPUExecutionProvider']
        )
    except Exception as e:
        print("Помилка ініціалізації ONNX Runtime:", e)
        return None
    
    # Відкриття зображення та конвертація в RGB
    img = Image.open(image_path).convert('RGB').resize((64, 64))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
    
    # Інференс
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    try:
        result = session.run([output_name], {input_name: img_array})[0]
        class_idx = np.argmax(result)
        return class_idx
    except Exception as e:
        print("Помилка інференсу:", e)
        return None

if __name__ == "__main__":
    image_path = "test_image.png"  # Шлях до зображення
    try:
        predicted_class = predict(image_path)
        if predicted_class is not None:
            print(f"Предбачений клас: {predicted_class}")
    except Exception as e:
        print("Помилка:", e)