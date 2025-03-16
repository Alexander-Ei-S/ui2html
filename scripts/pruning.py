import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow_model_optimization.sparsity import keras as sparsity

# Кастомні об'єкти для ігнорування параметра 'groups'
custom_objects = {
    'DepthwiseConv2D': lambda **kwargs: tf.keras.layers.DepthwiseConv2D(**{k: v for k, v in kwargs.items() if k != 'groups'})
}

# Завантаження моделі з ігноруванням 'groups'
model = load_model("models/ui_classifier_v2.h5", custom_objects=custom_objects)

# Налаштування прюнінгу
pruning_params = {
    'pruning_schedule': sparsity.PolynomialDecay(
        initial_sparsity=0.30,
        final_sparsity=0.70,
        begin_step=0,
        end_step=1000
    )
}

# Застосування прюнінгу
pruned_model = sparsity.prune_low_magnitude(model, **pruning_params)
pruned_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Перетренування
pruned_model.fit(train_generator, epochs=10, validation_data=val_generator)

# Збереження у форматі SavedModel
pruned_model.save("models/ui_classifier_pruned", save_format="tf")