import unittest

class TestCalculator(unittest.TestCase):

    # Test cases for addition
    def test_add_positive_numbers(self):
        self.assertEqual(3 + 4, 7)

    def test_add_negative_and_positive_number(self):
        self.assertEqual(-1 + 1, 0)

    def test_add_negative_numbers(self):
        self.assertEqual(-1 - 1, -2)

    # Test cases for subtraction
    def test_subtract_positive_numbers(self):
        self.assertEqual(10 - 5, 5)

    def test_subtract_larger_number_from_smaller(self):
        self.assertEqual(2 - 3, -1)

    def test_subtract_negative_numbers(self):
        self.assertEqual(-1 - -1, 0)

if __name__ == '__main__':
    unittest.main()
