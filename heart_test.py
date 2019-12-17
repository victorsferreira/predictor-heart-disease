import heart
import unittest

class TestHeart(unittest.TestCase):
    def test_get_inputs(self):
        #Assert if inputs contains expected keys
        inputs = heart.get_inputs(["val1=1"], ["val1"])
        self.assertDictEqual(inputs, {"val1": 1})

        #Assert if inputs ignores extra keys
        inputs = heart.get_inputs(["val1=1", "val2=2"], ["val1"])
        self.assertDictEqual(inputs, {"val1": 1})

#python3 -m unittest heart_test