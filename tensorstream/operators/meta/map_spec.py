import numpy as np
import tensorflow as tf

from tensorstream.streamable import Stream, stream_to_tensor
from tensorstream.operators.meta.map import Map
from tensorstream.operators.meta.factory import Factory
from tensorstream.operators.moving_average import SimpleMovingAverage
from tensorstream.operators.variation import Variation
from tensorstream.operators.meta.compose import Compose
from tensorstream.operators.tests import TestCase

class MapSpec(TestCase):
  def setUp(self):
    self.sheets = self.read_ods(
      self.from_test_res('map.ods', __file__))

  def test_map_skip_without_holes(self):
    s = self.sheets['vectorize']

    values = s[['Value 0', 'Value 1', 'Value 2']].replace(r'\s*', np.nan, regex=True)
    sma_outputs = s[['SMA4 0', 'SMA4 1', 'SMA4 2']].replace(r'\s*', np.nan, regex=True)

    values_ph = tf.placeholder(tf.float32)
    v = Map(SimpleMovingAverage(4), size=3)
    o, _ = stream_to_tensor(v(Stream(values_ph)))

    with tf.Session() as sess:
      output = sess.run(o, {
        values_ph: values
      })

    np.testing.assert_almost_equal(output,
      sma_outputs.values, decimal=3)
