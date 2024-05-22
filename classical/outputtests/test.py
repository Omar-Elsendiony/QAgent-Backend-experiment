import unittest

def triangle(x:int)->str:
    if x>40 :
        return "x>40 yes" 
    else: 
        return "no x is not >40"
    


class TestClass(unittest.TestCase):
	def test_case_0(self):
		int_0=4
		self.assertEqual('no x is not >40',triangle(int_0))

	def test_case_1(self):
		int_0=54
		self.assertEqual('x>40 yes',triangle(int_0))

if __name__ == '__main__':
    unittest.main()
    