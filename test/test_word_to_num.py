import unittest
from numeric_vision.utils import word_to_num


class TestWordToNum(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(word_to_num("five")[0], 5)
        self.assertEqual(word_to_num("zero")[0], 0)
        self.assertEqual(word_to_num("one million")[0], 1000000)
        self.assertEqual(word_to_num("one billion")[0], 1000000000)
        self.assertEqual(word_to_num("five billion two thousand eight hundred nineteen")[0], 5000002819)
        self.assertEqual(word_to_num("two hundred sixty five")[0], 265)
        self.assertEqual(word_to_num("ten")[0], 10)

    def test_negative_numbers(self):
        self.assertEqual(word_to_num("minus two")[0], -2)
        self.assertEqual(word_to_num("minus point two")[0], -0.2)
        self.assertEqual(word_to_num("minus one million")[0], -1000000)
        self.assertEqual(word_to_num("minus two billion")[0], -2000000000)

    def test_decimals(self):
        self.assertEqual(word_to_num("point six")[0], 0.6)
        self.assertEqual(word_to_num("minus point six")[0], -0.6)
        self.assertEqual(word_to_num("point zero seven")[0], 0.07)

    
    def test_comma_separated_numbers(self):
        self.assertEqual(word_to_num("five, three, one"), [5, 3, 1])
        self.assertEqual(word_to_num("five,three,one"), [5, 3, 1])
        self.assertEqual(word_to_num("five ,three ,one"), [5, 3, 1])
        self.assertEqual(word_to_num("five, three ,one"), [5, 3, 1])
        self.assertEqual(word_to_num("five , point three , minus one"), [5, 0.3, -1])
        self.assertEqual(word_to_num("minus five billion ,point three, minus one"), [-5000000000, 0.3, -1])

if __name__ == '__main__':
    unittest.main()