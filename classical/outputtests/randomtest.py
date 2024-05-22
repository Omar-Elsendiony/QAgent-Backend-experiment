import unittest

def triangle(x:int)->str:
    if x>40 :
        return "x>40 yes" 
    else: 
        return "no x is not >40"
    


class TestClass(unittest.TestCase):
	def test_case_0(self):

		int_0=68
		self.assertEqual('x>40 yes',triangle(int_0))

	def test_case_1(self):

		int_0=57
		self.assertEqual('x>40 yes',triangle(int_0))

	def test_case_2(self):

		int_0=77
		self.assertEqual('x>40 yes',triangle(int_0))

	def test_case_3(self):

		int_0=49
		self.assertEqual('x>40 yes',triangle(int_0))

	def test_case_4(self):

		int_0=24
		self.assertEqual('no x is not >40',triangle(int_0))

	def test_case_5(self):

		int_0=93
		self.assertEqual('x>40 yes',triangle(int_0))

	def test_case_6(self):

		int_0=45
		self.assertEqual('x>40 yes',triangle(int_0))

	def test_case_7(self):

		int_0=43
		self.assertEqual('x>40 yes',triangle(int_0))

	def test_case_8(self):

		int_0=54
		self.assertEqual('x>40 yes',triangle(int_0))

	def test_case_9(self):

		int_0=4
		self.assertEqual('no x is not >40',triangle(int_0))

if __name__ == '__main__':
    unittest.main()
    