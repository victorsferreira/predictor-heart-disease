import unittest
# It is appending path, not at the beginning
import sys
import os
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(dir,'..','src/predictor'))
import heart

class TestHeart(unittest.TestCase):
    def test_get_inputs(self):
        #Assert if inputs contains expected keys
        inputs = heart.get_inputs(["val1=1"], ["val1"])
        self.assertDictEqual(inputs, {"val1": '1'})

        #Assert if inputs ignores extra keys
        inputs = heart.get_inputs(["val1=1", "val2=2"], ["val1"])
        self.assertDictEqual(inputs, {"val1": '1'})

#python3 -m unittest heart_test