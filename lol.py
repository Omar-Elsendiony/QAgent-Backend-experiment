feedback = """FFF....
======================================================================
FAIL: test_truncate_large_negative_float (__main__.TestTruncateNumber.test_truncate_large_negative_float)
Test truncating a large negative float
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<string>", line 60, in test_truncate_large_negative_float
AssertionError: 0.8765432089567184 != -0.123456789

======================================================================
FAIL: test_truncate_large_positive_float (__main__.TestTruncateNumber.test_truncate_large_positive_float)
Test truncating a large positive float
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<string>", line 54, in test_truncate_large_positive_float
AssertionError: 0.12345679104328156 != 0.123456789

======================================================================
FAIL: test_truncate_negative_float (__main__.TestTruncateNumber.test_truncate_negative_float)
Test truncating a negative float
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<string>", line 42, in test_truncate_negative_float
AssertionError: 0.5 != -0.5

----------------------------------------------------------------------
Ran 7 tests in 0.000s

FAILED (failures=3)

=====================
"""

generatedCode = """import unittest

class TestTruncateNumber(unittest.TestCase):

    def setUp(self):
        self.truncate_number = truncate_number

    def test_truncate_positive_integer(self):
        '''Test truncating a positive integer'''
        number = 10
        result = self.truncate_number(number)
        self.assertEqual(result, 0.0)

    def test_truncate_negative_integer(self):
        '''Test truncating a negative integer'''
        number = -10
        result = self.truncate_number(number)
        self.assertEqual(result, 0.0)

    def test_truncate_positive_float(self):
        '''Test truncating a positive float'''
        number = 3.5
        result = self.truncate_number(number)
        self.assertEqual(result, 0.5)

    def test_truncate_negative_float(self):
        '''Test truncating a negative float'''
        number = -3.5
        result = self.truncate_number(number)
        self.assertEqual(result, -0.5)

    def test_truncate_zero(self):
        '''Test truncating zero'''
        number = 0.0
        result = self.truncate_number(number)
        self.assertEqual(result, 0.0)

    def test_truncate_large_positive_float(self):
        '''Test truncating a large positive float'''
        number = 123456789.123456789
        result = self.truncate_number(number)
        self.assertEqual(result, 0.123456789)

    def test_truncate_large_negative_float(self):
        '''Test truncating a large negative float'''
        number = -123456789.123456789
        result = self.truncate_number(number)
        self.assertEqual(result, -0.123456789)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])()
"""
import re


def getEachTestCase(UnitTestsCode, functionNames):
    # split the test cases
    if len(functionNames) == 0:
        return UnitTestsCode
    classHeader = re.search(r"(class.*:)", UnitTestsCode)
    method_pattern = r"""
    (def\s+        # Match 'def' keyword followed by whitespace
    ({0})         # Capture method signature using a named capturing group (1) 
                   #  where {0} is replaced with the joined method names
    \(.*?\)     
    \s*:)\n        # Match whitespace, colon, and whitespace
    (.*?)          # Capture method body (non-greedy) - group (3)
    (?=\n\s*def|\n\Z) # Positive lookahead to ensure not followed by another 'def' or end of string
    """.format(
        "|".join(functionNames)
    )  # Replace {0} with joined method names
    tests = []
    matches = re.finditer(
        method_pattern, UnitTestsCode, flags=re.DOTALL | re.MULTILINE | re.VERBOSE
    )
    for functionmatch in matches:
        print(functionmatch)
        method_defintion = functionmatch.group(1)
        method_body = functionmatch.group(3)
        method_body_lines = method_body.split("\n")
        method_body = "\n".join(["\t" + line for line in method_body_lines])
        tests.append("\t" + method_defintion + "\n" + method_body)
    tests = "\n".join(tests)
    editPattern = """if __name__ == '__main__':"""
    index = tests.find(editPattern)
    if index != -1:
        mainCall = tests[index:]
        mainCall_lines = mainCall.split("\n")
        mainCall = "\n" + mainCall_lines[0] + "\n\t" + mainCall_lines[1].strip()
        tests = tests[:index] + mainCall  # Slice up to the index of the substring
    code = "\nimport unittest\n\n" + classHeader.group(0) + "\n" + tests
    return code


def getNonSucceedingTestcases(feedback):
    failed_tests = re.findall(r"FAIL: (.*) \(", feedback)
    error_tests = re.findall(r"ERROR: (.*) \(", feedback)
    return {"failed": failed_tests, "error": error_tests}


erroneous_tests = getNonSucceedingTestcases(feedback)
print(erroneous_tests["failed"] + erroneous_tests["error"])
total_tests = getEachTestCase(
    generatedCode, erroneous_tests["failed"] + erroneous_tests["error"]
)
print(total_tests)
