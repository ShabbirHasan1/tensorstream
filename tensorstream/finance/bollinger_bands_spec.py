import numpy as np
import tensorflow as tf

from tensorstream.finance.bollinger_bands import BollingerBands
from tensorstream.tests import TestCase

class BollingerBandsSpec(TestCase):
  def setUp(self):
    self.input_ts = self.read_csv(
      self.from_test_res('bollinger_bands.csv', __file__)).astype('float32')

  def test_bollinger_bands(self):
    values = tf.placeholder(tf.float32)
    bollinger_bands = BollingerBands(20, 2)
    bb_ts, _ = bollinger_bands(values)

    with tf.Session() as sess:
      output = sess.run(bb_ts, {
        values: self.input_ts['Price'],
      })

    np.testing.assert_almost_equal(output[0],
      self.input_ts['Lower Band'].values, decimal=3)
    np.testing.assert_almost_equal(output[1],
      self.input_ts['Middle Band'].values, decimal=3)
    np.testing.assert_almost_equal(output[2],
      self.input_ts['Upper Band'].values, decimal=3)