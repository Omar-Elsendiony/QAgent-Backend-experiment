import unittest



def generate_integers(a:int, b:int)->list[int]:
    lower = max(2, min(a, b))
    upper = min(8, max(a, b))

    return [i for i in range(lower, upper+1) if i % 2 == 0]


class TestClass(unittest.TestCase):
	def test_case_0(self):
		int_0=41
		int_1=22
		self.assertEqual([],generate_integers(int_0,int_1))

	def test_case_1(self):
		int_0=68
		int_1=51
		self.assertEqual([],generate_integers(int_0,int_1))

	def test_case_2(self):
		int_0=94
		int_1=31
		self.assertEqual([],generate_integers(int_0,int_1))

	def test_case_3(self):
		int_0=60
		int_1=18
		self.assertEqual([],generate_integers(int_0,int_1))

	def test_case_4(self):
		int_0=0
		int_1=55
		self.assertEqual([2, 4, 6, 8],generate_integers(int_0,int_1))

	def test_case_5(self):
		int_0=58
		int_1=57
		self.assertEqual([],generate_integers(int_0,int_1))

	def test_case_6(self):
		int_0=37
		int_1=18
		self.assertEqual([],generate_integers(int_0,int_1))

	def test_case_7(self):
		int_0=30
		int_1=50
		self.assertEqual([],generate_integers(int_0,int_1))

	def test_case_8(self):
		int_0=71
		int_1=23
		self.assertEqual([],generate_integers(int_0,int_1))

	def test_case_9(self):
		int_0=6
		int_1=29
		self.assertEqual([6, 8],generate_integers(int_0,int_1))

if __name__ == '__main__':
    unittest.main()
    