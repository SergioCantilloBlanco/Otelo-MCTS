import tensorflow as tf
from neuronal_network import board_to_tensor
from UCT_othello_agent import UCTOtelloAgent

from othello import OthelloGame
import numpy as np
model = tf.keras.models.load_model("othello_training_model.h5")

class NeuralUCTOtelloAgent(UCTOtelloAgent):


  def default_policy(self, game: OthelloGame, player):
    processed_state = board_to_tensor(game.board)
    processed_state = np.expand_dims(processed_state, axis=0)
    predictions = model.predict(processed_state, verbose=0)
    value = predictions[0][0]

    if player == 2:
      value = -value
    return value
