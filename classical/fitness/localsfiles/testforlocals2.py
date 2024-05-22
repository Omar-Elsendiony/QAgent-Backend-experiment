import unittest

def solve(s: str) -> str:
    from inspect import currentframe, getframeinfo
    JSONFile = 'D:/CUFE/grad project/gp2/classical/Unit-Tests-Generation/src/fitness/localsfiles/localslineno.txt'
    with open(JSONFile, 'w') as anotate_f:
        anotate_f.write('')
    flg = 0
    idx = 0
    new_str = list(s)
    for i in s:
        with open(JSONFile, 'a') as anotate_f:
            frameinfo = getframeinfo(currentframe())
            locals()['aha'] = frameinfo.lineno
            anotate_f.write(str(locals()))
            anotate_f.write('\n')
        if i.isalpha():
            new_str[idx] = i.swapcase()
            flg = 1
        idx += 1
    s = ''
    for i in new_str:
        s += i
    with open(JSONFile, 'a') as anotate_f:
        frameinfo = getframeinfo(currentframe())
        locals()['aha'] = frameinfo.lineno
        anotate_f.write(str(locals()))
        anotate_f.write('\n')
    if flg == 0:
        return s[len(s)::-1]
    return s

class TestClass(unittest.TestCase):

    def test_case_9(self):
        str_0 = '/--'
        self.assertEqual('--/', solve(str_0))
if __name__ == '__main__':
    unittest.main()