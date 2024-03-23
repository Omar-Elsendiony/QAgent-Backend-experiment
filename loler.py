import unittest

class TestTruncateNumber(unittest.TestCase):
    def test_truncate_negative_float(self):
        """Test truncating a negative float"""
        number = -3.5
        result = self.truncate_number(number)
        self.assertEqual(result, -0.5)

    def test_truncate_large_positive_float(self):
        """Test truncating a large positive float"""
        number = 123456789.123456789
        result = self.truncate_number(number)
        self.assertEqual(result, 0.123456789)

    def test_truncate_large_negative_float(self):
        """Test truncating a large negative float"""
        number = -123456789.123456789
        result = self.truncate_number(number)
        self.assertEqual(result, -0.123456789)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"])()
