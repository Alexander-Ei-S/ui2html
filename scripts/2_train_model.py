import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import os

# Конфігурація
IMG_SIZE = (64, 64)
BATCH_SIZE = 8  # Зменшено для малого датасету
EPOCHS = 30
DATA_PATH = "dataset/processed"

# Перевірка наявності даних
if not os.path.exists(DATA_PATH) or len(os.listdir(DATA_PATH)) == 0:
    raise FileNotFoundError(f"Папка {DATA_PATH} порожня або не існує!")

# Підготовка даних
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATA_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_generator = train_datagen.flow_from_directory(
    DATA_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

# Перевірка класів
if len(train_generator.class_indices) == 0:
    raise ValueError("Не знайдено жодного класу! Перевірте структуру директорій.")

# Побудова моделі
model = models.Sequential([
    layers.Input(shape=(*IMG_SIZE, 3)),  # Фіксуємо попередження про input_shape
    layers.Conv2D(16, (3,3), activation="relu"),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(32, (3,3), activation="relu"),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dense(len(train_generator.class_indices), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Навчання
history = model.fit(
    train_generator,
    steps_per_epoch=max(1, train_generator.samples // BATCH_SIZE),
    validation_data=val_generator,
    validation_steps=max(1, val_generator.samples // BATCH_SIZE),
    epochs=EPOCHS
)

# Збереження моделі
model.save("models/ui_classifier_v2.h5")

# Візуалізація
plt.figure(figsize=(12,4))
plt.subplot(1,2,1)
plt.plot(history.history["accuracy"], label="Train Accuracy")
plt.plot(history.history["val_accuracy"], label="Val Accuracy")
plt.title("Training Metrics")
plt.legend()

plt.subplot(1,2,2)
plt.plot(history.history["loss"], label="Train Loss")
plt.plot(history.history["val_loss"], label="Val Loss")
plt.legend()
plt.savefig("docs/results/training_metrics.png")