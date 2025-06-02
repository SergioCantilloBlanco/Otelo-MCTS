import tensorflow as tf
from neuronal_network import board_to_tensor
from UCT_othello_agent import UCTOtelloAgent

from othello import OthelloGame

model = tf.keras.models.load_model("othello_training_model.h5")

class UCTOtelloAgent(UCTOtelloAgent):
  

  def default_policy(self, game: OthelloGame, player):
    processed_state = board_to_tensor(game.state)
    predictions = model.predict(processed_state, verbose=0)
    value = predictions[0][0]
    return value

