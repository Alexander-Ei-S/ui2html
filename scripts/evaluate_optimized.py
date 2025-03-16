import tensorflow as tf
import numpy as np
from sklearn.metrics import classification_report

# Оцінка прюнінгової моделі
pruned_model = tf.keras.models.load_model("models/ui_classifier_pruned.h5")
pruned_loss, pruned_acc = pruned_model.evaluate(test_generator)
print(f"Прюнінгована модель:\nAccuracy: {pruned_acc}\nLoss: {pruned_loss}")

# Оцінка квантованої моделі (TFLite)
interpreter = tf.lite.Interpreter(model_path="models/ui_classifier_quantized.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

y_true = []
y_pred = []

for i in range(len(test_generator)):
    img, label = test_generator[i]
    y_true.extend(np.argmax(label, axis=1))
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_details[0]['index'])
    y_pred.extend(np.argmax(pred, axis=1))

print("Звіт для квантованої моделі:")
print(classification_report(y_true, y_pred, target_names=test_generator.class_indices.keys()))