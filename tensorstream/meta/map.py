import tensorflow as tf

from tensorstream.helpers.map_fn import map_fn
from tensorstream.streamable import MetaStreamable

class Map(MetaStreamable):
  def __init__(self, operator, size):
    super().__init__()
    self.size = size
    self.operator = operator

  def properties(self, *inputs):
    placeholders, initial_state = self.operator.properties(*inputs)

    def dimensions(x):
      dim = tf.ones([tf.size(tf.shape(x))], dtype=tf.int32)
      return tf.concat([[self.size], dim], axis=0)
  
    return placeholders, map_fn(initial_state, [initial_state],
      lambda x: tf.tile(tf.expand_dims(x, axis=0), dimensions(x)))
 
  def step(self, inputs, prev_state):
    state_dtype = map_fn(prev_state, [prev_state], lambda x: x.dtype) 

    # Get operator output type.
    op_value, _ = self.operator(inputs[0], streamable=False)
    output_dtype = map_fn(op_value, [op_value], lambda o: o.dtype)

    def apply_op(inputs_states):
      return self.operator(
        inputs=inputs_states[0],
        state=inputs_states[1],
        streamable=False
      )

    outputs, next_state = tf.map_fn(
      apply_op,
      (inputs, prev_state),
      dtype=(output_dtype, state_dtype)
    )
    return outputs, next_state
