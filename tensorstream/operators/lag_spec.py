import numpy as np
import tensorflow as tf

from tensorstream.streamable import Stream, stream_to_tensor
from tensorstream.operators.lag import Lag
from tensorstream.operators.tests import TestCase

class LagSpec(TestCase):
  def setUp(self):
    self.input_ts = self.read_csv(
      self.from_test_res('lag.csv')).astype('float32')

  def test_lag(self):
    values = tf.placeholder(tf.float32)
    values_stream = Stream(values)
    buffer_ts, _ = stream_to_tensor(Lag(3)(values_stream))

    with tf.Session() as sess:
      output = sess.run(buffer_ts, { values: self.input_ts['Value'] })

    np.testing.assert_almost_equal(output,
      self.input_ts['Delayed'].values, decimal=3)
