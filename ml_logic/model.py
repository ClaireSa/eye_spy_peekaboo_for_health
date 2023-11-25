from tensorflow import keras
from keras import Model, Sequential, layers, regularizers
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Input, concatenate
from keras.callbacks import EarlyStopping
import numpy as np
from typing import Tuple
from keras.callbacks import EarlyStopping


def initialize_model(input_shape: tuple) -> Model:
    """
    Initialize the Neural Network with random weights
    """
    image_input = Input(shape=(224, 224, 3))
    x = Conv2D(32, (3, 3), activation='relu')(image_input)
    x = MaxPooling2D(2, 2)(x)
    x = Flatten()(x)


    row_input = Input(shape=input_shape)
    y = Dense(64, activation='relu')(row_input)

    combined = concatenate([x, y])

    z = Dense(12, activation='relu')(combined)
    z = Dense(64, activation='relu')(z)
    z = Dense(1, activation='sigmoid')(z)


    model = Model(inputs=[image_input, row_input], outputs=z)

    print("✅ Model initialized")

    return model



def compile_model(model: Model, learning_rate=0.0005) -> Model:
    """
    Compile the Neural Network
    """
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    print("✅ Model compiled")

    return model



def train_model(model: Model,
        X: np.ndarray,
        y: np.ndarray,
        batch_size=32,
        patience=2,
        validation_data=None, #([eval_images, X_eval], y_eval) #override validation split
        validation_split=0.3
    ) -> Tuple[Model, dict]:
    """
    Fit the model and return a tuple (fitted_model, history)
    """
    es = EarlyStopping(
    monitor="val_loss",
    patience=patience,
    restore_best_weights=True,
    verbose=0
    )

    history = model.fit(
    X,
    y,
    validation_data=validation_data,
    epochs=100,
    batch_size=batch_size,
    callbacks=[es],
    verbose=1
    )

    #print(f"✅ Model trained on {len(X)} rows with min val MAE: {round(np.min(history.history['val_mae']), 2)}")

    return model, history
