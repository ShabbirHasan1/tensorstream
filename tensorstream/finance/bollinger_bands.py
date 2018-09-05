import tensorflow as tf

from tensorstream.streamable import Streamable
from tensorstream.finance.moving_average import SimpleMovingAverage
from tensorstream.finance.moving_standard_deviation import MovingStandardDeviation

class BollingerBands(Streamable):
  def __init__(self, n, k, dtype=tf.float32, shape=()):
    super().__init__((dtype,) * 3, (shape,) * 3)
    self.k = k
    self.sma = SimpleMovingAverage(n, dtype=dtype, shape=shape)
    self.msd_op = MovingStandardDeviation(n, dtype=dtype, shape=shape)
    self.initial_state = ( 
      self.msd_op.initial_state,
      self.sma.initial_state
    )

  def step(self, value, volatility_state, sma_state):
    sma_output, sma_state = self.sma(value, state=sma_state, streamable=False)
    volatility_output, volatility_state = self.msd_op(value, state=volatility_state, streamable=False)

    middle_band = sma_output
    lower_band = sma_output - volatility_output * self.k
    upper_band = sma_output + volatility_output * self.k
    return (lower_band, middle_band, upper_band), (volatility_state, sma_state)