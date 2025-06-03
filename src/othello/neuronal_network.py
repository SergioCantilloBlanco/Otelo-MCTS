import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models


def create_othello_model():
    model = models.Sequential()
    model.add(layers.Input(shape=(8, 8, 3)))
    model.add(layers.Conv2D(64, (3, 3), padding="same", activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(128, (3, 3), padding="same", activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(64, (3, 3), padding="same", activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dense(1, activation="tanh"))
    return model



def board_to_tensor(board):
    tensor = np.zeros((8, 8, 3), dtype=np.float32)
    tensor[:, :, 0] = (board == 0)  # canal 0: casillas vacías
    tensor[:, :, 1] = (board == 1)  # canal 1: fichas blancas
    tensor[:, :, 2] = (board == 2)  # canal 2: fichas negras
    return tensor



def train():
    labeled_data = np.load("labeled_game_states.npy", allow_pickle=True)

    X = np.array([board_to_tensor(board) for board, _ in labeled_data])
    y = np.array([label for _, label in labeled_data], dtype=np.float32)

    print(len(X))
    print(len(y))

    model = create_othello_model()
    model.compile(optimizer="adam", loss=tf.keras.losses.Huber(), metrics=['mean_squared_error', 'mae'])
    model.summary()

    model.fit(X, y, epochs=150, batch_size=32, validation_split=0.1)
    model.save("othello_training_model.h5")

if __name__ == "__main__":
    train()
