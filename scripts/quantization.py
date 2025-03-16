# scripts/quantization.py
import tensorflow as tf
from tensorflow_model_optimization.sparsity import keras as sparsity

# Реєстрація кастомних об'єктів
custom_objects = {
    'PruneLowMagnitude': sparsity.prune_low_magnitude,
    'UpdatePruningStep': sparsity.UpdatePruningStep,
    'PruningPolicy': sparsity.PruningPolicy,
    'PrunableLayer': sparsity.PrunableLayer
}

# Завантаження моделі з SavedModel
with tf.keras.utils.custom_object_scope(custom_objects):
    model = tf.keras.models.load_model("models/ui_classifier_pruned")

# Конвертація у TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Збереження моделі
with open("models/ui_classifier_quantized.tflite", "wb") as f:
    f.write(tflite_model)

print("Квантування завершено!")