import random
import unittest

class TestHelloWorld(unittest.TestCase):

    def test_fail(self):
        self.assertEqual(1,0)

if __name__ == '__main__':
    unittest.main()