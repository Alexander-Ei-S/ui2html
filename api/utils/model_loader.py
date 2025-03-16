import onnxruntime as ort
import numpy as np
from PIL import Image

session = ort.InferenceSession(
    "models/ui_classifier.onnx",
    providers=['CPUExecutionProvider']  # Для універсальності
)

def predict_ui_element(image: Image.Image) -> str:
    # Попередня обробка зображення
    image = image.resize((64, 64)).convert("RGB")
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)

    # Передбачення
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: img_array})[0]
    class_idx = np.argmax(result)

    # Мапування класів (приклад)
    classes = {0: "button", 1: "input", 2: "card"}
    return classes.get(class_idx, "unknown")